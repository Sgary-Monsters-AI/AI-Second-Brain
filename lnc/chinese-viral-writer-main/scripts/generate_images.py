#!/usr/bin/env python3
"""
Universal Article Image Generation Script - Using Gemini REST API

Usage:
    python generate_images.py <prompts.json>

The prompts JSON file should be located in output/<article-folder>/ directory,
and generated images will be saved to output/<article-folder>/images/ directory.

JSON Format (two supported formats):

Format 1: New structured format (recommended)
{
    "article": {
        "title": "Article Title",
        "language": "Chinese",
        "sections": ["Section 1", "Section 2"]
    },
    "images": [
        {
            "type": "cover-wechat",
            "category": "cover",
            "platform": "wechat",
            "aspect_ratio": "2.35:1",
            "caption": "Cover - WeChat",
            "prompt": "Full prompt..."
        },
        {
            "type": "section-1",
            "category": "section",
            "section_index": 1,
            "aspect_ratio": "4:3",
            "caption": "Section 1 Illustration",
            "content": "Section content for template..."
        }
    ]
}

Format 2: Legacy array format (backward compatible)
[
    {
        "type": "cover-wechat",
        "caption": "Cover - WeChat",
        "prompt": "Full prompt..."
    }
]

Supported templates:
- cover: Pencil sketch style cover images
- section: Black and white comic manuscript style
- infographic: Hand-drawn cartoon style infographics
"""

import os
import sys
import json
import re
import base64
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not found")
    sys.exit(1)


# =============================================================================
# Image Prompt Templates
# =============================================================================

# Cover image template - Pencil sketch style
COVER_TEMPLATE = """1. 风格调性
   极简主义手绘素描，传统艺术风格，原始而细腻，纸上作品。强调手工质感和质朴美学。

2. 视觉逻辑
   平面二维视角，中心化对称构图。留白是构图的重要组成部分，主体孤立于背景之上。线条是有机的、非几何的。

3. 视觉渲染
   - 线条: 精细的石墨铅笔线条，带有手绘的自然抖动和压力变化，非数字化硬边。
   - 材质: 明显的粗糙纸张纹理，展现出纸张的纤维感。介质为石墨/铅笔。
   - 光影: 极简光影，主要通过轮廓线和少量排线来暗示形体，无复杂光源或投影。

4. 色彩系统
   - 单色调
   - 核心色: 石墨灰
   - 背景色: 灰白纸张色
   - 无其他色彩

5. 负向约束推导
   严禁数字绘画的平滑感，严禁矢量线条，严禁彩色，严禁照片级真实感，严禁复杂背景或场景，严禁 3D 渲染，严禁厚重颜料纹理

6. 画面内容
   {content}

7. 画面比例
   {aspect_ratio}"""

# Section illustration template - Black and white comic manuscript style
SECTION_TEMPLATE = """1. 风格调性
   极简主义黑白漫画手稿风格。核心气质是原生的、粗糙的、稀疏的、表现主义的速写。强调留白与高对比度的视觉张力，带有独立图画小说的艺术实验感。

2. 视觉逻辑
   - 构图模式：多格漫画页面排版。使用带有圆角的手绘不规则边框将画面分割为不同的面板（Panel）。
   - 空间构建：极其平面化的二维视角。不追求透视准确性，通过线条的疏密排列和剪影来暗示空间关系。利用大量负空间（Negative Space）构成画面主体。

3. 视觉渲染
   - 线条技法：极具手感和偶然性的线条。线条不闭合，边缘粗糙。
   - 材质质感：高对比度，无中间调。

4. 色彩系统
   - 单色系统。
   - 背景色：米白色/灰白色的纸张基调 。
   - 前景色：灰黑色

5. 负向约束推导
   严禁出现任何彩色或灰阶。严禁使用平滑的矢量线条、数字渐变或喷枪效果。避免精确的几何形状、直线尺规作图痕迹以及写实风格的光影和细节描绘。

6. 故事内容
   请基于以上风格，绘制如下内容的小故事，使用相同的语言（中文或者英文）,横版（4:3）构图：
   {content}"""

# Infographic template - Hand-drawn cartoon style
INFOGRAPHIC_TEMPLATE = """请根据输入内容提取核心主题与要点，生成一张卡通风格的信息图：
采用手绘风格，横版（4:3）构图。
加入少量简洁的卡通元素、图标或名人画像，增强趣味性和视觉记忆。
所有图像、文字必须使用手绘风格，没有写实风格图画元素。
除了专有名词外，其他文字使用{language}
drawing rules: no title

内容：
{content}"""


def get_prompt_from_template(category: str, content: str, **kwargs) -> str:
    """
    Generate a full prompt from a category and content.

    Args:
        category: One of 'cover', 'section', 'infographic'
        content: The content description to fill into the template
        **kwargs: Additional template parameters (aspect_ratio, language)

    Returns:
        The complete prompt string
    """
    if category == "cover":
        aspect_ratio = kwargs.get("aspect_ratio", "16:9")
        return COVER_TEMPLATE.format(content=content, aspect_ratio=aspect_ratio)
    elif category == "section":
        return SECTION_TEMPLATE.format(content=content)
    elif category == "infographic":
        language = kwargs.get("language", "Chinese")
        return INFOGRAPHIC_TEMPLATE.format(content=content, language=language)
    else:
        # For unknown categories, return content as-is (backward compatibility)
        return content


def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize prompt text to handle newlines, paragraph separators, and special characters.

    This function:
    - Normalizes various line break formats (CRLF, CR, LF) to single LF
    - Collapses multiple consecutive newlines into double newlines (paragraph breaks)
    - Strips leading/trailing whitespace from each line
    - Removes excessive whitespace while preserving intentional spacing
    - Handles special Unicode characters that might cause issues
    """
    if not prompt:
        return prompt

    # Normalize line endings: CRLF -> LF, CR -> LF
    text = prompt.replace('\r\n', '\n').replace('\r', '\n')

    # Replace paragraph separator (U+2029) and line separator (U+2028) with newlines
    text = text.replace('\u2029', '\n\n').replace('\u2028', '\n')

    # Split into lines and strip each line
    lines = [line.strip() for line in text.split('\n')]

    # Collapse multiple empty lines into single empty line (preserving paragraph breaks)
    collapsed_lines = []
    prev_empty = False
    for line in lines:
        is_empty = len(line) == 0
        if is_empty:
            if not prev_empty:
                collapsed_lines.append('')
            prev_empty = True
        else:
            collapsed_lines.append(line)
            prev_empty = False

    # Join with single newlines
    text = '\n'.join(collapsed_lines)

    # Strip leading/trailing whitespace from the entire text
    text = text.strip()

    # Collapse multiple spaces into single space (but preserve newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    return text


def generate_image(prompt: str, filename: str, images_dir: Path) -> str:
    """Generate image using Gemini REST API"""
    print(f"Generating: {filename}...")

    # Sanitize the prompt to handle newlines and special characters
    clean_prompt = sanitize_prompt(prompt)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": clean_prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    headers = {"Content-Type": "application/json"}

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode())

        # Extract image
        for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                image_data = base64.b64decode(part["inlineData"]["data"])
                filepath = images_dir / filename
                with open(filepath, "wb") as f:
                    f.write(image_data)
                print(f"✓ Saved: {filepath}")
                return str(filepath)

        print(f"✗ {filename} generation failed: No image returned")
        return None

    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"✗ {filename} generation failed: HTTP {e.code}")
        print(f"  Error details: {error_body[:200]}")
        return None
    except Exception as e:
        print(f"✗ {filename} generation failed: {e}")
        return None


def get_filename_from_type(image_type: str) -> str:
    """Generate filename from image type"""
    # Convert type to filename, e.g., "cover-wechat" -> "cover-wechat.png"
    return f"{image_type}.png"


def load_prompts_json(json_path: Path) -> tuple:
    """
    Load prompts JSON file.

    Supports two formats:
    1. New structured format: {"article": {...}, "images": [...]}
    2. Legacy array format: [{"type": "...", "prompt": "..."}]

    Returns:
        Tuple of (article_info, processed_images)
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Detect format
    if isinstance(data, dict) and "images" in data:
        # New structured format
        article_info = data.get("article", {})
        images_data = data["images"]
    elif isinstance(data, list):
        # Legacy array format
        article_info = {}
        images_data = data
    else:
        raise ValueError("JSON file must be an object with 'images' array or a direct array")

    # Get article language for templates
    article_language = article_info.get("language", "Chinese")

    processed_items = []

    for i, item in enumerate(images_data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} must be an object")
        if "type" not in item:
            raise ValueError(f"Item at index {i} missing 'type' field")

        image_type = item["type"]
        category = item.get("category", "")
        caption = item.get("caption", image_type)
        aspect_ratio = item.get("aspect_ratio", "4:3")

        # Determine prompt
        if "prompt" in item:
            # Full prompt provided
            prompt = item["prompt"]
        elif "content" in item:
            # Use template based on category
            content = item["content"]
            prompt = get_prompt_from_template(
                category,
                content,
                aspect_ratio=aspect_ratio,
                language=article_language
            )
        else:
            raise ValueError(f"Item at index {i} must have 'prompt' or 'content' field")

        processed_item = {
            "type": image_type,
            "category": category,
            "caption": caption,
            "prompt": prompt
        }
        processed_items.append(processed_item)

    return article_info, processed_items


def print_available_templates():
    """Print available template types"""
    print("\nAvailable template categories:")
    print("-" * 50)
    templates_info = {
        "cover": "Cover images - Pencil sketch style, various aspect ratios",
        "section": "Section illustrations - Black and white comic manuscript, 4:3",
        "infographic": "Infographics - Hand-drawn cartoon style, 4:3"
    }
    for name, desc in templates_info.items():
        print(f"  {name}: {desc}")
    print()


def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_images.py <prompts.json>")
        print()
        print("The prompts JSON file should be located in output/<article-folder>/ directory,")
        print("and generated images will be saved to output/<article-folder>/images/ directory.")
        print_available_templates()
        print("JSON format example (new structured format):")
        print('''
{
    "article": {
        "title": "Article Title",
        "language": "Chinese",
        "sections": ["Section 1", "Section 2"]
    },
    "images": [
        {
            "type": "cover-wechat",
            "category": "cover",
            "platform": "wechat",
            "aspect_ratio": "2.35:1",
            "caption": "Cover - WeChat",
            "content": "Article theme description..."
        },
        {
            "type": "section-1",
            "category": "section",
            "section_index": 1,
            "aspect_ratio": "4:3",
            "caption": "Section 1 Illustration",
            "content": "Section content for story..."
        }
    ]
}
''')
        sys.exit(1)

    # Check for --templates flag
    if sys.argv[1] == "--templates":
        print_available_templates()
        sys.exit(0)

    json_path = Path(sys.argv[1]).resolve()

    if not json_path.exists():
        print(f"Error: File does not exist: {json_path}")
        sys.exit(1)

    # Determine output directory (images subdirectory of JSON file's directory)
    output_dir = json_path.parent
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Load prompts
    try:
        article_info, prompts = load_prompts_json(json_path)
    except Exception as e:
        print(f"Error: Failed to load prompts file: {e}")
        sys.exit(1)

    print("=" * 60)
    print("Starting image generation")
    if article_info.get("title"):
        print(f"Article: {article_info['title']}")
    print(f"Prompts file: {json_path}")
    print(f"Output directory: {images_dir}")
    print(f"Image count: {len(prompts)}")
    print("=" * 60)

    # Print image list summary
    print("\n📝 Image list:\n")
    for i, item in enumerate(prompts):
        caption = item.get("caption", item["type"])
        category = item.get("category", "")
        category_str = f"[{category}]" if category else ""
        print(f"  {i+1}. {category_str} [{item['type']}] {caption}")

    print("\n" + "=" * 60)
    print("Generating images...")
    print("=" * 60)

    results = []
    total_tasks = len(prompts)

    # Generate all images
    for i, item in enumerate(prompts):
        image_type = item["type"]
        caption = item.get("caption", image_type)
        prompt = item["prompt"]
        filename = get_filename_from_type(image_type)

        print(f"\n[{i+1}/{total_tasks}] {caption}")
        path = generate_image(prompt, filename, images_dir)
        results.append((caption, path))

    print("\n" + "=" * 60)
    print("Image generation complete!")
    print("=" * 60)

    success = sum(1 for _, p in results if p)
    print(f"\nSuccess: {success}/{total_tasks}")
    print(f"Image directory: {images_dir}")

    for title, path in results:
        status = "✓" if path else "✗"
        print(f"  {status} {title}")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success > 0 else 1)
