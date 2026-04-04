# 文章配图提示词模板

本文件定义了文章配图的四种风格及其对应的提示词模板。使用 `gemini-3-pro-image-preview` 模型生成图片。

## 环境配置

图片生成需要配置环境变量：

```bash
export GEMINI_API_KEY=your-gemini-api-key-here
```

**获取 API Key：** https://aistudio.google.com/app/apikey

---

## 配图类型与默认风格

| 类型 | 默认风格 | 长宽比 | 说明 |
|-----|---------|--------|------|
| 封面图 | 素描（dankoe 用版画） | 按平台要求 | 文章开头，体现核心主题 |
| 插图 | 素描 | 16:9 | 章节配图，辅助理解 |
| 信息图 | 卡通 | 16:10 | 数据/概念可视化 |

**封面图风格规则：**
- **默认**：使用素描风格（sketch）
- **dankoe 人设**：使用版画风格（engraving），且内容需转换为超现实/科幻/神秘场景

**风格选择原则：** 默认风格仅供参考，应根据文章内容和调性选择最合适的风格。

| 内容类型 | 推荐风格 | 说明 |
|---------|---------|------|
| 深度思考、哲理、批判 | 素描（默认）/ 版画（dankoe） | dankoe 人设专用版画风格 |
| 日常叙事、温情、记录 | 素描 | 默认封面图风格 |
| 故事、场景、情节 | 手绘 | 适合叙事类内容 |
| 数据、流程、概念 | 卡通 | 适合信息图 |

---

## 一、素描风格

**适用场景：** 封面图、插图。日常叙事、温情故事、个人反思类内容。

### 提示词模板

```
1. 风格调性
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
   {内容描述}

7. 画面比例
   {长宽比}
```

---

## 二、手绘风格

**适用场景：** 插图。故事性内容、场景叙述、情节展示。

### 提示词模板

```
1. 风格调性
   极简主义黑白漫画手稿风格。核心气质是原生的、粗糙的、稀疏的、表现主义的速写。强调留白与高对比度的视觉张力，带有独立图画小说的艺术实验感。

2. 视觉逻辑
   - 构图模式：多格漫画页面排版。使用带有圆角的手绘不规则边框将画面分割为不同的面板（Panel）。
   - 空间构建：极其平面化的二维视角。不追求透视准确性，通过线条的疏密排列和剪影来暗示空间关系。利用大量负空间（Negative Space）构成画面主体。

3. 视觉渲染
   - 线条技法：极具手感和偶然性的线条。线条不闭合，边缘粗糙。
   - 材质质感：高对比度，无中间调。

4. 色彩系统
   - 单色系统。
   - 背景色：米白色/灰白色的纸张基调。
   - 前景色：灰黑色

5. 负向约束推导
   严禁出现任何彩色或灰阶。严禁使用平滑的矢量线条、数字渐变或喷枪效果。避免精确的几何形状、直线尺规作图痕迹以及写实风格的光影和细节描绘。

6. 故事内容
   请基于以上风格，绘制如下内容的小故事，使用相同的语言（中文或者英文）：
   {内容描述}

7. 画面比例
   {长宽比}
```

---

## 三、卡通风格

**适用场景：** 信息图。数据展示、概念解释、流程说明。

### 提示词模板

```
请根据输入内容提取核心主题与要点，生成一张卡通风格的信息图：
采用手绘风格，{长宽比}构图。
加入少量简洁的卡通元素、图标或名人画像，增强趣味性和视觉记忆。
所有图像、文字必须使用手绘风格，没有写实风格图画元素。
除了专有名词外，其他文字使用{文章语言}
drawing rules: no title

内容：
{信息内容}
```

---

## 四、版画风格

**适用场景：**
- **dankoe 人设封面图**（必须使用）
- 插图：深度思考、哲理探讨、批判性内容、史诗感叙事

**注意：** 版画风格现在**仅用于 dankoe 人设的封面图**。其他品牌的封面图默认使用素描风格。

### 提示词模板

```
A highly detailed, monochrome engraving style illustration depicting {内容描述}.

The artwork is rendered strictly in binary black ink on aged white paper, resembling a vintage woodcut or scratchboard print. There are no grey tones, only pure black and white.

Shading, texture, and volume are expertly achieved through a combination of dense cross-hatching lines, intricate stippling (dot work), and swirling line patterns. Stark, high-contrast chiaroscuro lighting creates dramatic silhouettes and deep shadows. The overall atmosphere is gritty, serious, and textured, with an epic or surreal quality.

Aspect ratio: {长宽比}
```

### dankoe 人设：超现实场景转换原则（必须遵循）

使用版画风格生成 dankoe 人设封面图时，**必须**将文章主题转换为超现实、科幻或神秘的视觉场景，而非直接描绘文章内容。

**转换流程：**
```
文章核心主题 → 识别抽象概念 → 转换为具象视觉隐喻 → 添加超现实元素
```

**转换示例表：**

| 原始主题 | 超现实视觉场景 |
|---------|---------------|
| 职业焦虑 | 一个巨大的石头脑袋漂浮在云端，脑袋顶部像火山一样喷发出许多微小的复古建筑 |
| 信息过载 | 一个穿着破旧长袍的孤独宇航员，站在一个巨大的、布满发光符文的古代遗迹门前 |
| AI 取代 | 人与机器人的镜像对视，镜子的边框由数据流构成 |
| 时间流逝 | 沙漏中困住了整座城市，正在缓缓下沉 |
| 选择困境 | 一个孤独的身影站在分岔路口，每条路通向不同的维度空间 |
| 专注与注意力 | 一个头部是棱镜的人形，将散射的光线折射成一束激光 |
| 技能叠加 | 一个人攀爬由相互连接的齿轮和书籍构成的高塔 |
| 打破常规 | 一个人从自己的大理石雕像中破壳而出 |
| 逃离传统道路 | A figure emerging from a cracked marble statue of a businessman, surrounded by floating geometric shapes |
| 复利效应 | A human climbing an impossible M.C. Escher-style staircase made of interconnected books and gears |
| 信息时代专注 | A lone figure in a small boat navigating through a sea of floating digital screens and symbols |
| 打破默认设置 | A person standing before a giant control panel with levers labeled "default" being switched off |

**超现实场景特征：**
- 超大尺度对比（巨大的头颅、微型的城市）
- 不可能的物理结构（埃舍尔式阶梯、漂浮物体）
- 元素错位（宇航员 + 古代遗迹、人体 + 机械）
- 象征性空间（维度门、镜像世界、数据海洋）
- 孤独的人物形象（单人站立、攀爬、面对）

---

## 封面图比例（按平台）

| 平台 | 比例 | 文件名 |
|-----|------|--------|
| 微信公众号 | 2.35:1 | `cover-wechat.png` |
| X Articles | 3:1 | `cover-x-articles.png` |
| 小红书 | 3:4 | `cover-xiaohongshu.png` |
| LinkedIn | 1.86:1 | `cover-linkedin.png` |

---

## prompts.json 文件格式

每篇文章生成的 `prompts.json` 文件包含所有需要生成的图片提示词，保存到 `output/<article-folder>/prompts.json`。

### 完整结构示例

```json
{
  "article": {
    "title": "文章标题",
    "language": "Chinese",
    "sections": ["章节1标题", "章节2标题", "章节3标题"]
  },
  "images": [
    {
      "type": "cover-wechat",
      "category": "cover",
      "platform": "wechat",
      "style": "engraving",
      "aspect_ratio": "2.35:1",
      "caption": "封面图描述",
      "prompt": "..."
    },
    {
      "type": "illustration-1",
      "category": "illustration",
      "section_index": 1,
      "style": "sketch",
      "aspect_ratio": "16:9",
      "caption": "图片标题/说明",
      "prompt": "..."
    },
    {
      "type": "infographic-1",
      "category": "infographic",
      "style": "cartoon",
      "aspect_ratio": "16:10",
      "caption": "信息图描述",
      "prompt": "..."
    }
  ]
}
```

### 图片分类

| 分类 | category | 默认风格 | 长宽比 |
|-----|----------|---------|--------|
| 封面图 | `cover` | 版画 | 按平台 |
| 插图 | `illustration` | 素描 | 16:9 |
| 信息图 | `infographic` | 卡通 | 16:10 |

### 风格标识

| 风格 | style 值 |
|-----|----------|
| 素描 | `sketch` |
| 手绘 | `hand-drawn` |
| 卡通 | `cartoon` |
| 版画 | `engraving` |

---

## API 调用规范

### Gemini API 直连

```python
import urllib.request
import json
import base64

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_image(prompt: str) -> bytes:
    """使用 Gemini API 生成图片"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode())

    for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])

    return None
```

### 命令行使用

```bash
# 生成所有配图
python scripts/generate_images.py output/<article-folder>/prompts.json
```
