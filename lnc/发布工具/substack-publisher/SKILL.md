---
name: substack-publisher
description: Publish newsletter articles to Substack as drafts. Use when "publish to substack", "create substack draft", "post newsletter to substack", "substack draft".
allowed-tools: Read, Glob, Bash, AskUserQuestion
---

# Substack Publisher

## What This Does

Takes a Markdown newsletter article and creates a beautiful draft in Substack, preserving all formatting (headers, bold, tables, code blocks, links). You review the draft in Substack, add images, and publish when ready.

## Prerequisites

### One-Time Setup

1. **Set a password on your Substack account** (if using magic links):
   - Go to Substack Settings → Account → Set password

2. **Add environment variables** to `~/.zshrc`:
   ```bash
   export SUBSTACK_EMAIL="your-email@example.com"
   export SUBSTACK_PASSWORD="your-password"
   export SUBSTACK_PUBLICATION_URL="https://thelittlebluereport.substack.com"
   ```

3. **Reload shell**: `source ~/.zshrc`

4. **Install the library** (first time only):
   ```bash
   pip install python-substack
   ```

### Verify Setup

Run the auth check before first use:
```bash
python3 ~/Documents/GitHub/powerhouse-lab/skills/substack-publisher/tools/check_auth.py
```

## Instructions

### PHASE 1: Locate the Article

When user says "publish to substack" or similar:

1. If they provide a file path, use that
2. If they mention an article name, search Zettelkasten:
   ```
   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/
   ```
3. Look for files starting with "Newsletter Draft -" or matching their description

Read the file to confirm it's the right article.

### PHASE 2: Extract Metadata

Parse the article for:

**Title:** Look for first `# Heading` or use filename (minus date)
**Subtitle:** Look for second `## Heading` or first bold line after title
**Body:** Everything after the subtitle

If frontmatter exists (between `---` markers), extract:
- `title:`
- `subtitle:`
- Any other metadata

### PHASE 3: Preview (Dry Run)

Show the user what will be created:

```
Ready to create Substack draft:

Title: [extracted title]
Subtitle: [extracted subtitle]
Body preview: [first 150 characters]...

Word count: [X] words
Estimated read time: [X] minutes
```

### PHASE 4: Confirm

Use AskUserQuestion to confirm before creating the draft.

Ask: "Create this draft in Substack?"
- Options: "Yes, create draft" / "Edit title/subtitle first" / "Cancel"

If they want to edit, let them provide new title/subtitle, then confirm again.

### PHASE 5: Create Draft

Run the publish script:

```bash
python3 ~/Documents/GitHub/powerhouse-lab/skills/substack-publisher/tools/publish_draft.py \
  --file "/path/to/article.md" \
  --title "The Title" \
  --subtitle "The Subtitle"
```

Parse the output for the draft URL.

### PHASE 6: Report Success

Tell the user:

```
Draft created successfully!

View your draft: [URL]

Next steps:
1. Open the link above
2. Add any images
3. Preview and publish when ready
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Authentication failed" | Check SUBSTACK_EMAIL and SUBSTACK_PASSWORD in ~/.zshrc |
| "Publication not found" | Verify SUBSTACK_PUBLICATION_URL is correct |
| "Rate limited" | Wait 60 seconds and try again |
| "File not found" | Confirm the markdown file path exists |

## Examples

**User:** "Hey, publish my newsletter about the 45 minutes to 45 seconds thing"

**Claude:**
1. Searches Zettelkasten for matching file
2. Finds "Newsletter Draft - 45 Minutes to 45 Seconds - 2026-01-15.md"
3. Extracts title: "45 Minutes to 45 Seconds"
4. Extracts subtitle: "45 Minutes of Prep Work. Done in 45 Seconds."
5. Shows preview, asks for confirmation
6. Creates draft, returns URL

**User:** "Create a substack draft from ~/Documents/article.md"

**Claude:**
1. Reads the specified file
2. Extracts metadata
3. Confirms with user
4. Creates draft

## Roadmap

**Current (MVP):**
- Markdown → Substack draft
- Title/subtitle extraction
- Dry-run confirmation

**Planned:**
- Image uploading
- One-click publish (skip draft)
- Scheduling posts
- Audience targeting (free vs paid)
