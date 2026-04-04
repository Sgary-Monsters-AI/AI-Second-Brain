# Substack Content Types Reference

This documents the Substack JSON format used by the python-substack library.

## Basic Structure

All content is added via `post.add(block)` where block is a dictionary.

## Content Types

### Paragraph

```python
post.add({
    'type': 'paragraph',
    'content': 'Plain text here'
})

# With formatting
post.add({
    'type': 'paragraph',
    'content': [
        {'content': 'Regular text '},
        {'content': 'bold text', 'marks': [{'type': 'strong'}]},
        {'content': ' more regular'}
    ]
})
```

### Heading

```python
post.add({
    'type': 'heading',
    'attrs': {'level': 2},  # 1-6
    'content': 'Header Text'
})
```

### Horizontal Rule

```python
post.add({'type': 'horizontal_rule'})
```

### Code Block

```python
post.add({
    'type': 'codeBlock',
    'attrs': {'language': 'python'},
    'content': 'def hello():\n    print("world")'
})
```

### Blockquote

```python
post.add({
    'type': 'blockquote',
    'content': [
        {'type': 'paragraph', 'content': 'Quoted text here'}
    ]
})
```

### Bullet List

```python
post.add({
    'type': 'bulletList',
    'content': [
        {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': 'Item 1'}]},
        {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': 'Item 2'}]}
    ]
})
```

### Ordered List

```python
post.add({
    'type': 'orderedList',
    'content': [
        {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': 'First'}]},
        {'type': 'listItem', 'content': [{'type': 'paragraph', 'content': 'Second'}]}
    ]
})
```

### Table

```python
post.add({
    'type': 'table',
    'content': [
        {
            'type': 'tableRow',
            'content': [
                {'type': 'tableHeader', 'content': [{'type': 'paragraph', 'content': 'Col 1'}]},
                {'type': 'tableHeader', 'content': [{'type': 'paragraph', 'content': 'Col 2'}]}
            ]
        },
        {
            'type': 'tableRow',
            'content': [
                {'type': 'tableCell', 'content': [{'type': 'paragraph', 'content': 'Data 1'}]},
                {'type': 'tableCell', 'content': [{'type': 'paragraph', 'content': 'Data 2'}]}
            ]
        }
    ]
})
```

### Image

```python
# Remote URL
post.add({
    'type': 'captionedImage',
    'src': 'https://example.com/image.jpg'
})

# Local file (auto-uploaded)
post.add({
    'type': 'captionedImage',
    'src': '/path/to/local/image.jpg'
})
```

## Inline Marks

Use within content arrays:

| Mark Type | Example |
|-----------|---------|
| `strong` | Bold text |
| `em` | Italic text |
| `code` | Inline code |
| `link` | Hyperlink (requires `href`) |

```python
# Bold
{'content': 'bold', 'marks': [{'type': 'strong'}]}

# Italic
{'content': 'italic', 'marks': [{'type': 'em'}]}

# Code
{'content': 'code', 'marks': [{'type': 'code'}]}

# Link
{'content': 'click here', 'marks': [{'type': 'link', 'href': 'https://example.com'}]}

# Combined (bold + link)
{'content': 'bold link', 'marks': [{'type': 'strong'}, {'type': 'link', 'href': 'https://...'}]}
```

## Post Metadata

```python
from substack.post import Post

post = Post(
    title="My Post Title",
    subtitle="The subtitle or hook",
    user_id=user_id
)

# Additional options in the draft
draft = post.get_draft()
draft['audience'] = "everyone"  # or "only_paid", "founding", "only_free"
draft['comments'] = "everyone"  # or "none", "only_paid"
```
