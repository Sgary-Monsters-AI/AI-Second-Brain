#!/usr/bin/env python3
"""
Substack Draft Publisher

Takes a Markdown file and creates a draft post on Substack.
Preserves formatting: headers, bold, italic, links, code blocks, lists, tables.

Usage:
    python3 publish_draft.py --file article.md
    python3 publish_draft.py --file article.md --title "Custom Title" --subtitle "Custom Sub"
    python3 publish_draft.py --file article.md --dry-run

Environment variables required:
    SUBSTACK_EMAIL - Your Substack login email
    SUBSTACK_PASSWORD - Your Substack password
    SUBSTACK_PUBLICATION_URL - Full URL (e.g., https://thelittlebluereport.substack.com)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Union, List, Dict, Tuple


def check_environment():
    """Verify required environment variables exist.

    Supports two auth methods:
    1. Cookie auth (preferred): SUBSTACK_COOKIE + SUBSTACK_PUBLICATION_URL
    2. Password auth: SUBSTACK_EMAIL + SUBSTACK_PASSWORD + SUBSTACK_PUBLICATION_URL
    """
    publication_url = os.environ.get("SUBSTACK_PUBLICATION_URL")
    cookie = os.environ.get("SUBSTACK_COOKIE")
    email = os.environ.get("SUBSTACK_EMAIL")
    password = os.environ.get("SUBSTACK_PASSWORD")

    if not publication_url:
        print("ERROR: Missing SUBSTACK_PUBLICATION_URL")
        print('\nAdd to ~/.zshrc:')
        print('  export SUBSTACK_PUBLICATION_URL="https://yourpub.substack.com"')
        sys.exit(1)

    # Cookie auth takes priority (more reliable)
    if cookie:
        return {
            "auth_method": "cookie",
            "cookie": cookie,
            "publication_url": publication_url,
        }

    # Fall back to password auth
    if email and password:
        return {
            "auth_method": "password",
            "email": email,
            "password": password,
            "publication_url": publication_url,
        }

    # Neither method configured
    print("ERROR: No authentication configured")
    print("\nOption 1 - Cookie auth (recommended):")
    print('  export SUBSTACK_COOKIE="substack.sid=your_cookie_value"')
    print("\nOption 2 - Password auth:")
    print('  export SUBSTACK_EMAIL="your-email"')
    print('  export SUBSTACK_PASSWORD="your-password"')
    print("\nThen run: source ~/.zshrc")
    sys.exit(1)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter if present, return (metadata, body)."""
    metadata = {}
    body = content

    if content.startswith("---"):
        end_match = re.search(r'\n---\s*\n', content[3:])
        if end_match:
            frontmatter = content[3:end_match.start() + 3]
            body = content[end_match.end() + 3:].strip()

            # Simple YAML parsing for common fields
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')

    return metadata, body


def extract_title_subtitle(content: str) -> tuple[str, str, str]:
    """Extract title and subtitle from markdown content."""
    lines = content.split('\n')
    title = ""
    subtitle = ""
    body_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip empty lines and notes at the start
        if not stripped or stripped.startswith("**Note:**"):
            continue

        # First # heading is title
        if stripped.startswith('# ') and not title:
            title = stripped[2:].strip()
            body_start = i + 1
            continue

        # Skip horizontal rules
        if stripped == '---':
            continue

        # Second ## heading or first significant line after title is subtitle
        if title and not subtitle:
            if stripped.startswith('## '):
                subtitle = stripped[3:].strip()
                body_start = i + 1
                break
            elif stripped:
                # Use first paragraph as subtitle
                subtitle = stripped
                body_start = i + 1
                break

    # Body is everything after title/subtitle extraction
    body = '\n'.join(lines[body_start:]).strip()

    # Clean up subtitle if it's a header marker
    if subtitle == '---':
        subtitle = ""

    return title, subtitle, body


def markdown_to_substack_content(markdown: str) -> list:
    """
    Convert Markdown to Substack's content format.
    Returns a list of content blocks for post.add().
    """
    content_blocks = []
    lines = markdown.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped in ['---', '***', '___']:
            content_blocks.append({'type': 'horizontal_rule'})
            i += 1
            continue

        # Headers (## through ######)
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            level = len(header_match.group(1))
            text = header_match.group(2)
            content_blocks.append({
                'type': 'heading',
                'level': level,
                'content': parse_inline_formatting(text)
            })
            i += 1
            continue

        # Code block (fenced)
        if stripped.startswith('```'):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            content_blocks.append({
                'type': 'codeblock',
                'language': lang or 'text',
                'content': '\n'.join(code_lines)
            })
            i += 1  # Skip closing ```
            continue

        # Blockquote
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            content_blocks.append({
                'type': 'blockquote',
                'content': parse_inline_formatting(' '.join(quote_lines))
            })
            continue

        # Unordered list
        if re.match(r'^[-*+]\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^[-*+]\s', lines[i].strip()):
                item_text = re.sub(r'^[-*+]\s+', '', lines[i].strip())
                items.append(parse_inline_formatting(item_text))
                i += 1
            content_blocks.append({
                'type': 'bullet_list',
                'items': items
            })
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                items.append(parse_inline_formatting(item_text))
                i += 1
            content_blocks.append({
                'type': 'ordered_list',
                'items': items
            })
            continue

        # Table
        if '|' in stripped and i + 1 < len(lines) and re.match(r'^[\|\s\-:]+$', lines[i + 1].strip()):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            content_blocks.append(parse_table(table_lines))
            continue

        # Checkbox item (task list)
        checkbox_match = re.match(r'^[-*]\s*\[([ xX])\]\s*(.+)$', stripped)
        if checkbox_match:
            checked = checkbox_match.group(1).lower() == 'x'
            text = checkbox_match.group(2)
            # Treat as regular paragraph with checkbox emoji
            prefix = "[x] " if checked else "[ ] "
            content_blocks.append({
                'type': 'paragraph',
                'content': parse_inline_formatting(prefix + text)
            })
            i += 1
            continue

        # Regular paragraph
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not is_block_start(lines[i]):
            para_lines.append(lines[i].strip())
            i += 1

        content_blocks.append({
            'type': 'paragraph',
            'content': parse_inline_formatting(' '.join(para_lines))
        })

    return content_blocks


def is_block_start(line: str) -> bool:
    """Check if a line starts a new block element."""
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith('#'):
        return True
    if stripped.startswith('```'):
        return True
    if stripped.startswith('> '):
        return True
    if re.match(r'^[-*+]\s', stripped):
        return True
    if re.match(r'^\d+\.\s', stripped):
        return True
    if stripped in ['---', '***', '___']:
        return True
    if '|' in stripped:
        return True
    return False


def parse_inline_formatting(text: str) -> Union[list, str]:
    """
    Parse inline formatting (bold, italic, links, code) into Substack format.
    Returns either a string (plain text) or a list of content objects.
    """
    # If no formatting, return plain string
    if not re.search(r'[\*_`\[]', text):
        return text

    parts = []
    current_pos = 0

    # Pattern for: **bold**, *italic*, `code`, [text](url)
    pattern = r'(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|\[([^\]]+)\]\(([^)]+)\))'

    for match in re.finditer(pattern, text):
        # Add text before this match
        if match.start() > current_pos:
            parts.append({'content': text[current_pos:match.start()]})

        full_match = match.group(0)

        if full_match.startswith('**'):
            # Bold
            parts.append({
                'content': match.group(2),
                'marks': [{'type': 'strong'}]
            })
        elif full_match.startswith('*'):
            # Italic
            parts.append({
                'content': match.group(3),
                'marks': [{'type': 'em'}]
            })
        elif full_match.startswith('`'):
            # Inline code
            parts.append({
                'content': match.group(4),
                'marks': [{'type': 'code'}]
            })
        elif full_match.startswith('['):
            # Link
            parts.append({
                'content': match.group(5),
                'marks': [{'type': 'link', 'href': match.group(6)}]
            })

        current_pos = match.end()

    # Add remaining text
    if current_pos < len(text):
        parts.append({'content': text[current_pos:]})

    # If only one part with no marks, return plain string
    if len(parts) == 1 and 'marks' not in parts[0]:
        return parts[0]['content']

    return parts


def parse_table(lines: list) -> dict:
    """Parse a markdown table into a code block (Substack doesn't support native tables)."""
    # Convert table to ASCII-formatted text for code block display
    # First pass: determine column widths
    all_rows = []
    for i, line in enumerate(lines):
        # Skip separator row (|---|---|)
        if i == 1 and re.match(r'^[\|\s\-:]+$', line.strip()):
            continue
        cells = [cell.strip() for cell in line.strip().split('|')]
        cells = [c for c in cells if c]  # Remove empty cells from pipe delimiters
        all_rows.append(cells)

    if not all_rows:
        return {'type': 'paragraph', 'content': ''}

    # Calculate max width for each column
    num_cols = max(len(row) for row in all_rows)
    col_widths = [0] * num_cols
    for row in all_rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], len(cell))

    # Build formatted table text
    table_lines = []
    for row_idx, row in enumerate(all_rows):
        # Pad cells to column width
        padded = []
        for i in range(num_cols):
            cell = row[i] if i < len(row) else ''
            padded.append(cell.ljust(col_widths[i]))
        table_lines.append(' | '.join(padded))

        # Add separator after header row
        if row_idx == 0:
            separator = ['-' * w for w in col_widths]
            table_lines.append('-+-'.join(separator))

    return {
        'type': 'codeblock',
        'language': 'text',
        'content': '\n'.join(table_lines)
    }


def build_substack_post(title: str, subtitle: str, content_blocks: list):
    """Build a Substack post object from content blocks."""
    try:
        from substack import Api
        from substack.post import Post
    except ImportError:
        print("ERROR: python-substack not installed.")
        print("Run: pip install python-substack")
        sys.exit(1)

    creds = check_environment()

    # Authenticate based on available method
    if creds["auth_method"] == "cookie":
        api = Api(
            cookies_string=creds["cookie"],
            publication_url=creds["publication_url"],
        )
    else:
        api = Api(
            email=creds["email"],
            password=creds["password"],
            publication_url=creds["publication_url"],
        )

    user_id = api.get_user_id()

    # Create post
    post = Post(
        title=title,
        subtitle=subtitle,
        user_id=user_id
    )

    # Helper to convert content to Substack text nodes
    def to_text_nodes(content):
        """Convert content (string or list) to Substack text node format."""
        if isinstance(content, str):
            return [{'type': 'text', 'text': content}]
        elif isinstance(content, list):
            nodes = []
            for chunk in content:
                node = {'type': 'text', 'text': chunk.get('content', '')}
                marks = chunk.get('marks', [])
                if marks:
                    node['marks'] = []
                    for mark in marks:
                        m = {'type': mark.get('type')}
                        if mark.get('type') == 'link' and mark.get('href'):
                            m['attrs'] = {'href': mark.get('href')}
                        node['marks'].append(m)
                nodes.append(node)
            return nodes
        return []

    # Build content directly (library's add() doesn't handle nested structures)
    doc_content = []

    for block in content_blocks:
        block_type = block.get('type')

        if block_type == 'paragraph':
            doc_content.append({
                'type': 'paragraph',
                'content': to_text_nodes(block['content'])
            })

        elif block_type == 'heading':
            doc_content.append({
                'type': 'heading',
                'attrs': {'level': block['level']},
                'content': to_text_nodes(block['content'])
            })

        elif block_type == 'horizontal_rule':
            doc_content.append({'type': 'horizontalRule'})

        elif block_type == 'codeblock':
            doc_content.append({
                'type': 'codeBlock',
                'attrs': {'language': block.get('language', 'text')},
                'content': [{'type': 'text', 'text': block['content']}]
            })

        elif block_type == 'blockquote':
            doc_content.append({
                'type': 'blockquote',
                'content': [{
                    'type': 'paragraph',
                    'content': to_text_nodes(block['content'])
                }]
            })

        elif block_type == 'bullet_list':
            items = []
            for item in block['items']:
                items.append({
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': to_text_nodes(item)
                    }]
                })
            doc_content.append({'type': 'bulletList', 'content': items})

        elif block_type == 'ordered_list':
            items = []
            for item in block['items']:
                items.append({
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': to_text_nodes(item)
                    }]
                })
            doc_content.append({'type': 'orderedList', 'content': items})

        # Note: Tables are converted to codeblocks in parse_table() since
        # Substack's Tiptap editor doesn't support native table nodes

    # Set the draft body directly
    import json
    post.draft_body = {
        'type': 'doc',
        'content': doc_content
    }

    return api, post


def create_draft(title: str, subtitle: str, content_blocks: list) -> dict:
    """Create a draft post on Substack."""
    api, post = build_substack_post(title, subtitle, content_blocks)

    # Create draft
    draft = api.post_draft(post.get_draft())

    return draft


def main():
    parser = argparse.ArgumentParser(description="Create a Substack draft from Markdown")
    parser.add_argument("--file", "-f", required=True, help="Path to Markdown file")
    parser.add_argument("--title", "-t", help="Override title")
    parser.add_argument("--subtitle", "-s", help="Override subtitle")
    parser.add_argument("--dry-run", action="store_true", help="Show preview without creating draft")
    args = parser.parse_args()

    # Read file
    file_path = Path(args.file).expanduser()
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    content = file_path.read_text(encoding='utf-8')

    # Parse frontmatter
    metadata, body = parse_frontmatter(content)

    # Extract title/subtitle
    extracted_title, extracted_subtitle, body = extract_title_subtitle(body)

    # Use overrides or extracted values
    title = args.title or metadata.get('title') or extracted_title
    subtitle = args.subtitle or metadata.get('subtitle') or extracted_subtitle

    if not title:
        print("ERROR: Could not extract title. Use --title to specify.")
        sys.exit(1)

    # Convert to Substack format
    content_blocks = markdown_to_substack_content(body)

    # Calculate stats
    word_count = len(body.split())
    read_time = max(1, word_count // 200)

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN - Preview of Substack draft")
        print("=" * 60)
        print(f"\nTitle: {title}")
        print(f"Subtitle: {subtitle}")
        print(f"\nWord count: {word_count}")
        print(f"Estimated read time: {read_time} min")
        print(f"\nContent blocks: {len(content_blocks)}")
        print("\nBody preview (first 300 chars):")
        print("-" * 40)
        print(body[:300] + "..." if len(body) > 300 else body)
        print("-" * 40)
        print("\n[DRY RUN - No draft created]")
        sys.exit(0)

    # Check environment before attempting to create
    check_environment()

    print(f"Creating draft: {title}")
    print(f"Subtitle: {subtitle}")
    print(f"Content blocks: {len(content_blocks)}")

    try:
        draft = create_draft(title, subtitle, content_blocks)
        draft_id = draft.get('id')

        # Construct draft URL
        pub_url = os.environ["SUBSTACK_PUBLICATION_URL"].rstrip('/')
        draft_url = f"{pub_url}/publish/post/{draft_id}"

        print("\n" + "=" * 60)
        print("SUCCESS! Draft created.")
        print("=" * 60)
        print(f"\nDraft URL: {draft_url}")
        print(f"\nNext steps:")
        print("1. Open the link above")
        print("2. Add any images")
        print("3. Preview and publish when ready")

    except Exception as e:
        print(f"\nERROR creating draft: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
