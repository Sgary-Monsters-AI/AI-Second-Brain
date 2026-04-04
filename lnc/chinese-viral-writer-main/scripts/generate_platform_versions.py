#!/usr/bin/env python3
"""
Generate platform-specific versions from the original article.

Supports:
- WeChat Official Account (微信公众号)
- X (Twitter) Articles
- Xiaohongshu (小红书)

Usage:
    # Generate all platform versions
    python generate_platform_versions.py output/{dir}/article.md

    # Generate specific platform
    python generate_platform_versions.py output/{dir}/article.md --platform wechat
    python generate_platform_versions.py output/{dir}/article.md --platform x
    python generate_platform_versions.py output/{dir}/article.md --platform xiaohongshu

    # With custom images directory
    python generate_platform_versions.py output/{dir}/article.md --images-dir ./images
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional


# WeChat header templates
WECHAT_HEADER_TEMPLATES = [
    "下一篇就是你的赚钱灵感来源",
    "不错过任何一个搞钱机会",
    "每篇都是真金白银的经验",
    "你的独立开发之路从这里开始",
    "副业灵感每周更新",
    "程序员转型第一站",
]

# WeChat footer templates
WECHAT_FOOTER_TEMPLATES = [
    ("🚀 我们都在用勤劳忽略房间里的大象", "📬 关注「Roland」，产品认知和实战笔记，不打鸡血，只讲干货。"),
    ("💡 赚钱这件事，认知比努力更重要", "📬 关注「Roland」，一起搞副业、做产品、赚美金。"),
    ("🎯 方向对了，努力才有意义", "📬 点个关注，下一个产品灵感可能就在下一篇。"),
    ("🔥 别等万事俱备，先搞起来再说", "📬 关注我，看一个普通程序员怎么一步步搞到钱。"),
]

# WeChat author section (fixed)
WECHAT_AUTHOR_SECTION = """
---

##### 关于作者 | Roland


![](https://files.mdnice.com/user/25644/3a42e4d8-c789-4908-b2a2-a2fd14c2ac73.PNG =25%x)


我是 **Roland**，医学&经济学博士，现居澳洲。

这个号记录我的认知升级思维方式、跨领域实践和创业踩坑故事。

---
:::block-1
如果你想更系统了解我是怎么做副业赚钱的，推荐阅读我的电子笔记《搞到钱再说》——记录了从第一个想法到赚到第一桶金的全过程，适合对产品和出海感兴趣的你。

:::block-2
![](https://files.mdnice.com/user/25644/a1c6363b-eb16-45a7-a4f0-aaceceffbd7f.jpg)
:::
"""

# X CTA section (Chinese)
X_CTA_SECTION_CN = """
---

### 关注我

如果这篇文章对你有帮助，欢迎关注我的 X 账号 **@rwayne**，我会持续跨界思考、出海创业、AI 工具等内容。

👉 [Roland的思考日记](https://x.com/rwayne)
"""

# X CTA section (English)
X_CTA_SECTION_EN = """
---

### Follow Me

If you found this article helpful, follow me on X **@BuildWithJames** for more insights on product development, indie hacking, and AI tools.

👉 [Build With James](https://x.com/BuildWithJames)
"""

# LinkedIn CTA section
LINKEDIN_CTA_SECTION = """
---

### Connect With Me

If you enjoyed this article, let's connect on LinkedIn. I share insights on product development, indie hacking, and navigating the AI revolution.

👉 [James Gong on LinkedIn](https://www.linkedin.com/in/zifei/)
"""

# Xiaohongshu hashtag suggestions by topic
XIAOHONGSHU_HASHTAGS = {
    "程序员": ["#程序员", "#代码人生", "#独立开发者", "#技术人", "#码农日常"],
    "副业": ["#副业", "#搞钱", "#创业", "#被动收入", "#自由职业"],
    "AI": ["#AI工具", "#效率提升", "#工具推荐", "#ChatGPT", "#人工智能"],
    "职场": ["#职场", "#个人成长", "#认知升级", "#职业规划", "#干货分享"],
    "出海": ["#出海", "#海外创业", "#全球化", "#跨境", "#数字游民"],
}


def read_article(file_path: str) -> str:
    """Read article content from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_title(markdown: str) -> str:
    """Extract title from markdown (H1)."""
    match = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def remove_images(markdown: str) -> str:
    """Remove image references from markdown."""
    return re.sub(r'!\[([^\]]*)\]\([^)]+\)\n*', '', markdown)


def count_chinese_chars(text: str) -> int:
    """Count Chinese characters in text."""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def markdown_to_plain_text(markdown: str) -> str:
    """Convert markdown to plain text for Xiaohongshu."""
    text = markdown

    # Remove images
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)

    # Convert headers to plain text (remove #)
    text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)

    # Convert bold to plain text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)

    # Convert italic to plain text
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Convert links to just text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Convert blockquotes
    text = re.sub(r'^>\s*(.+)$', r'\1', text, flags=re.MULTILINE)

    # Keep list formatting but simplify
    text = re.sub(r'^-\s+', '• ', text, flags=re.MULTILINE)

    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)

    # Remove horizontal rules
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)

    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def generate_wechat_version(
    content: str,
    header_text: Optional[str] = None,
    footer_line1: Optional[str] = None,
    footer_line2: Optional[str] = None,
) -> str:
    """Generate WeChat Official Account version."""

    # Use default or provided header
    if header_text is None:
        header_text = WECHAT_HEADER_TEMPLATES[0]

    # Use default or provided footer
    if footer_line1 is None or footer_line2 is None:
        footer_line1, footer_line2 = WECHAT_FOOTER_TEMPLATES[0]

    # Build header
    header = f"""👆 **「关注」**加**「星标」**，{header_text}！

---

"""

    # Build footer
    footer = WECHAT_AUTHOR_SECTION + f"""
---
##### 下次灵感别错过

{footer_line1}

{footer_line2}
"""

    return header + content + footer


def generate_x_version(content: str, language: str = "cn") -> str:
    """
    Generate X (Twitter) Articles version.

    Args:
        content: Article content in Markdown
        language: "cn" for Chinese, "en" for English
    """
    cta = X_CTA_SECTION_EN if language == "en" else X_CTA_SECTION_CN
    return content + cta


def generate_linkedin_version(content: str) -> str:
    """
    Generate LinkedIn article version.

    Note: This expects English content. The content should be translated
    from Chinese to English before calling this function.
    """
    return content + LINKEDIN_CTA_SECTION


def generate_xiaohongshu_version(
    content: str,
    max_chars: int = 500,
    hashtags: Optional[list] = None,
) -> str:
    """
    Generate Xiaohongshu version.

    Note: This function prepares the plain text format.
    The actual content shortening to 500 chars should be done by AI
    to preserve meaning and create engaging copy.
    """
    # Convert to plain text
    plain_text = markdown_to_plain_text(content)

    # Remove title (first line if it looks like a title)
    lines = plain_text.split('\n')
    if lines and not lines[0].startswith(('•', '1.', '2.', '3.')):
        # Check if first non-empty line is likely a title
        for i, line in enumerate(lines):
            if line.strip():
                if len(line.strip()) < 50 and not line.strip().endswith(('。', '！', '？', '，')):
                    lines = lines[i+1:]
                break
    plain_text = '\n'.join(lines)

    # Generate default hashtags based on content keywords
    if hashtags is None:
        hashtags = detect_hashtags(plain_text)

    # Ensure max 5 hashtags
    hashtags = hashtags[:5]

    # Format hashtags
    hashtag_str = ' '.join(hashtags)

    # Add separator and hashtags
    result = plain_text.strip() + "\n\n---\n\n" + hashtag_str

    return result


def detect_hashtags(text: str) -> list:
    """Detect relevant hashtags based on content."""
    hashtags = []
    text_lower = text.lower()

    # Check for topic keywords
    if any(word in text_lower for word in ['程序员', '代码', '开发', '编程', 'cursor', 'vibe coding']):
        hashtags.extend(XIAOHONGSHU_HASHTAGS["程序员"][:2])

    if any(word in text_lower for word in ['副业', '赚钱', '搞钱', '收入', '创业']):
        hashtags.extend(XIAOHONGSHU_HASHTAGS["副业"][:2])

    if any(word in text_lower for word in ['ai', '人工智能', 'gpt', 'claude', '智能']):
        hashtags.extend(XIAOHONGSHU_HASHTAGS["AI"][:2])

    if any(word in text_lower for word in ['职场', '工作', '职业', '成长']):
        hashtags.extend(XIAOHONGSHU_HASHTAGS["职场"][:1])

    if any(word in text_lower for word in ['出海', '海外', '全球', '跨境']):
        hashtags.extend(XIAOHONGSHU_HASHTAGS["出海"][:1])

    # Remove duplicates while preserving order
    seen = set()
    unique_hashtags = []
    for tag in hashtags:
        if tag not in seen:
            seen.add(tag)
            unique_hashtags.append(tag)

    # If no hashtags detected, use defaults
    if not unique_hashtags:
        unique_hashtags = ["#干货分享", "#个人成长", "#认知升级"]

    return unique_hashtags[:5]


def save_version(content: str, output_path: str) -> None:
    """Save content to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate platform-specific article versions')
    parser.add_argument('article', help='Path to article.md file')
    parser.add_argument('--platform', choices=['wechat', 'x', 'x-en', 'xiaohongshu', 'linkedin', 'all', 'all-with-english'],
                       default='all', help='Target platform (default: all). Use "all-with-english" for all platforms including English versions.')
    parser.add_argument('--wechat-header', help='Custom WeChat header text')
    parser.add_argument('--wechat-footer1', help='Custom WeChat footer line 1')
    parser.add_argument('--wechat-footer2', help='Custom WeChat footer line 2')
    parser.add_argument('--hashtags', nargs='+', help='Custom hashtags for Xiaohongshu')
    parser.add_argument('--output-dir', help='Output directory (default: same as input)')
    parser.add_argument('--english-content', help='Path to English version of the article (for x-en and linkedin)')

    args = parser.parse_args()

    if not os.path.exists(args.article):
        print(f"Error: File not found: {args.article}", file=sys.stderr)
        sys.exit(1)

    # Read article content
    content = read_article(args.article)
    title = extract_title(content)

    # Read English content if provided
    english_content = None
    if args.english_content and os.path.exists(args.english_content):
        english_content = read_article(args.english_content)

    # Determine output directory
    input_dir = os.path.dirname(args.article)
    output_dir = args.output_dir or input_dir

    print(f"📄 Processing: {args.article}")
    print(f"📝 Title: {title}")
    print(f"📁 Output: {output_dir}")
    print()

    # Generate requested versions
    if args.platform == 'all':
        platforms = ['wechat', 'x', 'xiaohongshu']
    elif args.platform == 'all-with-english':
        platforms = ['wechat', 'x', 'x-en', 'xiaohongshu', 'linkedin']
    else:
        platforms = [args.platform]

    for platform in platforms:
        if platform == 'wechat':
            print("🔄 Generating WeChat version...")
            wechat_content = generate_wechat_version(
                content,
                header_text=args.wechat_header,
                footer_line1=args.wechat_footer1,
                footer_line2=args.wechat_footer2,
            )
            save_version(wechat_content, os.path.join(output_dir, 'wechat.md'))

        elif platform == 'x':
            print("🔄 Generating X Articles version (Chinese)...")
            x_content = generate_x_version(content, language="cn")
            save_version(x_content, os.path.join(output_dir, 'x-article.md'))

        elif platform == 'x-en':
            print("🔄 Generating X Articles version (English)...")
            if english_content:
                x_en_content = generate_x_version(english_content, language="en")
                save_version(x_en_content, os.path.join(output_dir, 'x-article-en.md'))
            else:
                print("⚠️  Note: English content not provided. Use --english-content or generate x-article-en.md manually.")
                print("   The English version should be translated from the Chinese X article.")
                # Create placeholder file
                placeholder = f"""# {title} (English Version)

> ⚠️ This is a placeholder. Please translate the Chinese X article to English.
>
> Steps:
> 1. Translate `x-article.md` to English
> 2. Save as `x-article-en.md`
> 3. Or provide --english-content parameter

{X_CTA_SECTION_EN}
"""
                save_version(placeholder, os.path.join(output_dir, 'x-article-en.md'))

        elif platform == 'linkedin':
            print("🔄 Generating LinkedIn version...")
            if english_content:
                linkedin_content = generate_linkedin_version(english_content)
                save_version(linkedin_content, os.path.join(output_dir, 'linkedin.md'))
            else:
                # Try to read from x-article-en.md if exists
                x_en_path = os.path.join(output_dir, 'x-article-en.md')
                if os.path.exists(x_en_path):
                    x_en_content = read_article(x_en_path)
                    # Remove X CTA and add LinkedIn CTA
                    x_en_content = x_en_content.replace(X_CTA_SECTION_EN.strip(), '').strip()
                    linkedin_content = generate_linkedin_version(x_en_content)
                    save_version(linkedin_content, os.path.join(output_dir, 'linkedin.md'))
                else:
                    print("⚠️  Note: English content not found. Generate x-article-en.md first, then linkedin.md.")
                    placeholder = f"""# {title} (LinkedIn Version)

> ⚠️ This is a placeholder. Please generate the English X article first.
>
> Steps:
> 1. Generate `x-article-en.md` (translate from Chinese)
> 2. Then run: python generate_platform_versions.py article.md --platform linkedin

{LINKEDIN_CTA_SECTION}
"""
                    save_version(placeholder, os.path.join(output_dir, 'linkedin.md'))

        elif platform == 'xiaohongshu':
            print("🔄 Generating Xiaohongshu version...")
            print("⚠️  Note: Xiaohongshu version needs AI to shorten to 500 chars")
            xhs_content = generate_xiaohongshu_version(
                content,
                hashtags=args.hashtags,
            )
            save_version(xhs_content, os.path.join(output_dir, 'xiaohongshu.txt'))

            # Print char count
            plain_text = markdown_to_plain_text(content)
            char_count = count_chinese_chars(plain_text)
            print(f"   Current: {char_count} chars (target: ≤500)")

    print()
    print("✨ Done!")


if __name__ == '__main__':
    main()
