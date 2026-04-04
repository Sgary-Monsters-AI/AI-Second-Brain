# Substack Publisher - Roadmap

## Shipped

| Version | Date | What Changed |
|---------|------|--------------|
| v1.0 | 2026-01-15 | Initial release - Markdown to Substack draft |

## Planned

- [ ] **Image uploading** - Upload local images and insert into post
- [ ] **One-click publish** - Skip draft, publish directly (with confirmation)
- [ ] **Scheduling** - Set publish date/time
- [ ] **Audience targeting** - Choose free, paid, or specific segments

## Ideas (Not Committed)

- Cross-post to multiple publications
- Template system for recurring formats
- Analytics integration (view stats after publish)
- Automatic social preview image generation

## What We've Learned

*To be filled in as we use the skill*

## Decision Log

| Date | Decision | Why |
|------|----------|-----|
| 2026-01-15 | Use python-substack library | Only maintained Python library for Substack API |
| 2026-01-15 | Draft-only for MVP | Safety first - always review before publishing |
| 2026-01-15 | Password auth over cookies | Simpler setup, cookies require browser export |
