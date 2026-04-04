# Substack Publisher - How It Works

## The One-Sentence Version

Write your newsletter in Markdown, say "publish to Substack", and get a beautiful draft ready for final review.

## Why This Exists

You write newsletters in Obsidian. They look great in Markdown - clean formatting, proper headers, nice tables.

But getting that into Substack? Copy-paste nightmare. Formatting breaks. Headers don't transfer. Tables turn into mush.

This skill is your publishing assistant. It takes your polished Markdown and creates a Substack draft that looks exactly how you intended. You add images, do a final review, and hit publish.

Think of it like having a layout person who takes your manuscript and typesets it perfectly - every time, in seconds.

## How You Use It

### Step 1: Write Your Newsletter

Write in Obsidian like you always do. Use Markdown formatting:
- `# Title` for your main headline
- `## Subtitle` for your hook
- `**bold**` for emphasis
- Tables, code blocks, whatever you need

### Step 2: Say the Magic Words

Tell Claude: "Publish my newsletter about [topic] to Substack"

Or: "Create a Substack draft from [filename]"

### Step 3: Confirm the Preview

Claude shows you:
- The title it extracted
- The subtitle
- A preview of the body
- Word count and read time

You confirm it looks right, or tweak the title/subtitle.

### Step 4: Get Your Draft

Claude creates the draft and gives you the URL. Open it in Substack, add any images, and you're ready to publish.

## The Technical Bit (For the Curious)

Under the hood, this uses an unofficial Python library that talks to Substack's API. It converts your Markdown into Substack's internal format (a JSON structure that defines paragraphs, headers, formatting, etc.).

The draft is created but NOT published - you always get final say before anything goes live.

## Safety Rails

- **Always creates a draft** - Never publishes directly
- **Confirms before sending** - You see exactly what will be created
- **Preserves your original** - The Markdown file is never modified
