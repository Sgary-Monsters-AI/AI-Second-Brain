# Substack Publisher - Technical Reference

## What It Does

Converts Markdown newsletter articles to Substack's format and creates drafts via the unofficial python-substack API. Preserves formatting including headers, bold/italic, links, code blocks, blockquotes, lists, and tables.

## Dependencies

**Tools required:** Read, Glob, Bash, AskUserQuestion

**Python packages:**
- `python-substack` - Unofficial Substack API client
- `markdown` - Markdown parsing (standard library fallback available)

**Environment variables:**
| Variable | Purpose |
|----------|---------|
| `SUBSTACK_EMAIL` | Your Substack login email |
| `SUBSTACK_PASSWORD` | Your Substack password (not magic link) |
| `SUBSTACK_PUBLICATION_URL` | Full URL like `https://thelittlebluereport.substack.com` |

## Architecture

```
User provides markdown file
        ↓
Extract title/subtitle from content
        ↓
Convert markdown → Substack JSON format
        ↓
POST to Substack API as draft
        ↓
Return draft URL for review
```

## API Details

**Authentication:** Email + password via `substack.Api()`. Magic link accounts must set a password first.

**Draft creation:** `api.post_draft(post.get_draft())` creates without publishing.

**Content format:** Substack uses a custom JSON schema:
```python
post.add({'type': 'paragraph', 'content': 'Text here'})
post.add({'type': 'heading', 'level': 2, 'content': 'Header'})
```

See `resources/content-types.md` for full format reference.

## Usage

**Trigger phrases:**
- "publish to substack"
- "create substack draft"
- "post newsletter to substack"
- "substack draft"

**CLI (direct):**
```bash
python3 tools/publish_draft.py --file article.md --title "Title" --subtitle "Sub"
python3 tools/publish_draft.py --file article.md --dry-run
```

## Testing

1. **Auth check:** `python3 tools/check_auth.py`
2. **Dry run:** `python3 tools/publish_draft.py --file test.md --dry-run`
3. **Full test:** Create draft, verify in Substack UI

## File Structure

```
skills/substack-publisher/
├── SKILL.md              # Skill instructions
├── tools/
│   ├── publish_draft.py  # Main script
│   └── check_auth.py     # Credential verification
├── docs/
│   ├── README.md         # This file
│   ├── GUIDE.md          # Business-friendly guide
│   └── ROADMAP.md        # Version history
└── resources/
    └── content-types.md  # Substack format reference
```

## Gotchas

- **Magic links:** Accounts using passwordless login need to set a password first
- **Rate limiting:** Keep requests to max 1/second
- **Unofficial API:** May break if Substack changes their internal API
- **Tables:** Substack has limited table support - may render differently
