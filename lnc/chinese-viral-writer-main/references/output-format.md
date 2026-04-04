# 文章输出规范

本文件定义了文章生成完成后的保存、预览和复制规范。

> **重要**：本规范已与引擎2统一，详见 [[统一输出格式规范]]

---

## 一、文件保存规范

### 目录结构

**统一输出路径**（与引擎2一致）：

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/
└── {YYYY-MM-DD}-{内容标题}/
    ├── index.md              # 元内容/原始文案（必需）
    ├── wechat.md             # 微信公众号版本（必需）
    ├── video-transcript.md   # 视频逐字稿（引擎1不生成）
    ├── x-cn.md               # X Articles 中文版（可选）
    ├── x-en.md               # X Articles 英文版（可选）
    ├── linkedin.md           # LinkedIn 版本（可选）
    ├── xhs-long.md           # 小红书长文版本（可选）
    ├── xhs-short.txt         # 小红书短文版本（可选）
    ├── promotion.md          # 传播素材（可选）
    ├── prompts.json          # 图片生成提示词（可选）
    └── _attachments/         # Obsidian 附件目录
        ├── cover-wechat.png    # 微信封面 (2.35:1)
        ├── cover-x.png         # X 封面 (3:1)
        ├── cover-xhs.png       # 小红书封面 (3:4)
        ├── cover-linkedin.png  # LinkedIn 封面 (1.86:1)
        ├── section-01.png      # 章节插图 1
        ├── section-02.png      # 章节插图 2
        ├── xhs-01.png          # 小红书卡片截图
        ├── xhs-02.png
        └── ...
```

### 文件命名规范

**目录名称：**

- 格式：`{YYYY-MM-DD}-{内容标题}`
- 示例：`2026-02-04-QS排名50和51真的有区别吗`
- 标题规则：保留完整标题，去除特殊符号（保留中文、英文、数字）

**图片命名：**

- 平台封面图：`cover-{平台}.png`（如 `cover-wechat.png`, `cover-x.png`, `cover-xhs.png`, `cover-linkedin.png`）
- 章节插图：`section-{序号}.png`（如 `section-01.png`, `section-02.png`）
- 小红书截图：`xhs-{序号}.png`（如 `xhs-01.png`, `xhs-02.png`）

### Markdown 文件格式

```markdown
# {文章标题}

![](./_attachments/cover-wechat.png)

{文章正文第一段}

{文章正文...}

## {章节标题 1}

![](./_attachments/section-01.png)

{章节内容...}

## {章节标题 2}

![](./_attachments/section-02.png)

{章节内容...}
```

---

## 二、预览规范

### 预览内容

文章完成后，必须展示完整的图文预览：

1. **封面预览**：显示封面图 + 文章标题
2. **正文预览**：渲染 Markdown 为可读格式
3. **图片预览**：内嵌显示所有生成的图片
4. **元信息**：显示字数统计、图片数量

### 预览格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 文章预览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[封面图预览]

# 文章标题

正文内容...

[章节插图预览]

## 章节标题

章节内容...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 统计信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 字数：{N} 字
- 图片：{M} 张（封面 1 + 章节 X + 信息图 Y）
- 保存位置：/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录名}/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 三、复制选项

### 提供三种复制格式

预览完成后，提供以下复制选项：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 复制选项
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 「复制纯文本」
   → 仅复制文字内容，不含图片引用
   → 适用于：纯文本编辑器、短信、即时通讯

2. 「复制 Markdown」
   → 复制完整 Markdown，含图片相对路径
   → 适用于：Markdown 编辑器、GitHub、语雀

3. 「复制 HTML」
   → 复制 HTML 格式，图片使用 base64 内嵌
   → 适用于：公众号编辑器、富文本编辑器

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 复制格式详解

#### 1. 纯文本格式

```
文章标题

正文第一段内容...

正文第二段内容...

章节标题

章节内容...
```

特点：

- 去除所有 Markdown 语法
- 去除图片引用
- 保留段落空行
- 保留标题层级（用空行分隔）

#### 2. Markdown 格式

```markdown
# 文章标题

![封面图](./_attachments/cover-wechat.png)

正文第一段内容...

## 章节标题

![章节插图](./_attachments/section-01.png)

章节内容...
```

特点：

- 完整的 Markdown 语法
- 图片使用相对路径引用
- 需要配合 images 目录使用

#### 3. HTML 格式（带内嵌图片）

```html
<h1>文章标题</h1>

<img
  src="data:image/png;base64,{封面图base64}"
  alt="封面图"
  style="max-width:100%;"
/>

<p>正文第一段内容...</p>

<h2>章节标题</h2>

<img
  src="data:image/png;base64,{章节插图base64}"
  alt="章节插图"
  style="max-width:100%;"
/>

<p>章节内容...</p>
```

特点：

- 图片使用 base64 编码内嵌
- 可直接粘贴到富文本编辑器
- 无需额外上传图片
- 文件较大（因为图片内嵌）

---

## 四、实现代码参考

### 保存文件

```python
import os
from datetime import datetime

def save_article(title: str, content: str, images: dict) -> str:
    """
    保存文章和图片

    Args:
        title: 文章标题
        content: Markdown 内容
        images: 图片字典 {"cover": bytes, "section-1": bytes, ...}

    Returns:
        保存目录路径
    """
    # 生成目录名
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c for c in title[:10] if c.isalnum() or c in "一二三四五六七八九十")
    dir_name = f"{date_str}-{safe_title}"
    dir_path = os.path.expanduser(f"/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{dir_name}")

    # 创建目录
    os.makedirs(f"{dir_path}/_attachments", exist_ok=True)

    # 保存 Markdown
    with open(f"{dir_path}/index.md", "w", encoding="utf-8") as f:
        f.write(content)

    # 保存图片
    for name, data in images.items():
        with open(f"{dir_path}/_attachments/{name}.png", "wb") as f:
            f.write(data)

    return dir_path
```

### 生成复制内容

```python
import base64
import re

def to_plain_text(markdown: str) -> str:
    """转换为纯文本"""
    # 移除图片
    text = re.sub(r"!\[.*?\]\(.*?\)", "", markdown)
    # 移除 Markdown 语法
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # 清理多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def to_html_with_embedded_images(markdown: str, images: dict) -> str:
    """转换为带内嵌图片的 HTML"""
    import markdown as md

    # 替换图片路径为 base64
    html_content = markdown
    for name, data in images.items():
        b64 = base64.b64encode(data).decode()
        old_ref = f"./_attachments/{name}.png"
        new_ref = f"data:image/png;base64,{b64}"
        html_content = html_content.replace(old_ref, new_ref)

    # 转换 Markdown 为 HTML
    html = md.markdown(html_content)
    return html
```

---

## 五、用户交互流程

### 完整流程示例

```
[文章生成完成]
     ↓
[自动保存文件]
     ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 文章已保存到 /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/2026-01-10-职场内卷真相/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ↓
[展示图文预览]
     ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 复制选项（请输入数字选择）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 复制纯文本
2. 复制 Markdown
3. 复制 HTML（含内嵌图片）
0. 跳过复制
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ↓
[用户选择后执行复制]
     ↓
✅ 已复制到剪贴板！
     ↓
[收集反馈]
```

---

## 六、多平台版本规范

详见 `references/platform-formats.md`

### 微信公众号版本 (wechat.md)

**用途**：直接复制到微信公众号后台或 mdnice 等排版工具

**结构**：

```markdown
👆 **「关注」**加**「星标」**，{引发关注的文案}！

---

{文章正文，含配图}

---

##### 关于作者 | Roland

{作者介绍}

---

##### 下次灵感别错过

{互动引导文案}
```

### X Articles 版本 (x-index.md)

**用途**：发布到 X (Twitter) Articles

**结构**：

```markdown
# {标题}

{文章正文，含配图}

---

### 关注我

如果这篇文章对你有帮助，欢迎关注我的 X 账号 **@rwayne**，我会持续分享产品开发、出海创业、AI 工具等内容。

👉 [Roland的思考日记](https://x.com/rwayne)
```

### 小红书版本 (xhs-short.txt)

**用途**：直接复制到小红书笔记编辑器

**格式要求**：

- 纯文本格式
- 字数 ≤ 500
- 不使用 Markdown 语法
- 只支持换行、分段、列表
- 末尾包含 ≤5 个 hashtag

**结构**：

```
{吸引眼球的开头}

{精简后的正文内容}

{核心观点总结}

---

#标签1 #标签2 #标签3
```

### 传播素材 (promotion.md)

**用途**：文章发布时的传播素材，包含摘要和各平台分享文案

**结构**：

```markdown
# 传播素材

## 文章摘要

{120 字以内的文章核心观点摘要}

## 朋友圈分享文案

{3-5 行口语化文案}
{引发好奇或共鸣}
{可带 1-2 个话题标签}
→ 点击阅读全文

## LinkedIn 分享文案

{English promotion text, 150 words or less}
{Professional but engaging tone}
{For LinkedIn's "Tell my network what your article is about" feature}

#Hashtag1 #Hashtag2 #Hashtag3
```

**LinkedIn 分享文案示例**：

```
AI is reshaping software development faster than most realize. In this article, I explore why 2026 might be the worst year to be "just a programmer" - and what the most valuable skill combo will be going forward.

Spoiler: It's not about writing better code. It's about learning to capture attention.

#IndieHacker #AI #Programming #ProductDevelopment #CareerAdvice
```

---

## 七、生成命令

### 生成所有平台版本

```bash
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md
```

### 生成单一平台版本

```bash
# 微信公众号
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform wechat

# X Articles
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform x

# 小红书
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform xiaohongshu
```

### 自定义文案

```bash
# 自定义微信头部文案
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --wechat-header "每篇都是真金白银的经验"

# 自定义小红书 hashtag
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --hashtags "#程序员" "#副业" "#搞钱"
```

---

## 八、注意事项

1. **图片大小**：HTML 格式因为内嵌 base64 图片，文件会较大，适合直接粘贴到编辑器
2. **路径兼容**：Markdown 格式使用相对路径，复制后需要保持目录结构
3. **编码问题**：所有文件使用 UTF-8 编码
4. **目录权限**：确保 /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布 目录有写入权限
5. **小红书字数**：脚本会提示当前字数，实际精简需要 AI 完成以保持语义
6. **X 发布**：需要 Premium Plus 订阅和 Playwright MCP 支持
