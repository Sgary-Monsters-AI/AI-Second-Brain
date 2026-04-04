# 多平台发布格式规范

本文件定义了将长文元内容转换为各平台发布版本的格式规范。

---

## 一、平台版本概述

| 平台                        | 格式     | 字数限制 | 语言 | 特殊要求                             |
| --------------------------- | -------- | -------- | ---- | ------------------------------------ |
| 微信公众号                  | Markdown | 无限制   | 中文 | 需插入配图、关注引导、作者介绍       |
| X (Twitter) Articles 中文版 | Markdown | 无限制   | 中文 | 需添加关注 CTA                       |
| X (Twitter) Articles 英文版 | Markdown | 无限制   | 英文 | 基于中文版翻译，英文 CTA             |
| LinkedIn                    | Markdown | 无限制   | 英文 | 基于英文 X 版本，LinkedIn CTA        |
| 小红书                      | 纯文本   | ≤500 字  | 中文 | 只支持换行/分段/列表，需添加 hashtag |

---

## 二、微信公众号版本

### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/wechat.md
```

### 结构规范

```markdown
👆 **「关注」**加**「星标」**，{引发关注的文案}！

---

{文章正文，包含插入的配图}

---

##### 关于作者 | Roland

我是 **Roland**，医学&经济学博士，现居澳洲。

这个号记录我的认知升级思维方式、跨领域实践和创业踩坑故事。

---

:::block-1
如果你想更系统了解我是怎么做副业赚钱的，推荐阅读我的电子笔记《搞到钱再说》——记录了从第一个想法到赚到第一桶金的全过程，适合对产品和出海感兴趣的你。

:::block-2
![](https://files.mdnice.com/user/25644/a1c6363b-eb16-45a7-a4f0-aaceceffbd7f.jpg)
:::

---

##### 下次灵感别错过

{引发关注和互动的文案}
```

### 头部引导文案示例

以下是可选的头部引导文案，根据文章主题选择或创作新的：

- 下一篇就是你的赚钱灵感来源
- 不错过任何一个搞钱机会
- 每篇都是真金白银的经验
- 你的独立开发之路从这里开始
- 副业灵感每周更新
- 程序员转型第一站

### 尾部互动文案示例

以下是可选的尾部互动文案，根据文章主题选择或创作新的：

```markdown
🚀 我们都在用勤劳忽略房间里的大象

📬 关注「Roland」，认知升级和实战笔记，不打鸡血，只讲干货。
```

其他可选文案：

```markdown
💡 赚钱这件事，认知比努力更重要

📬 关注「Roland」，一起搞副业、做产品、赚美金。
```

```markdown
🎯 方向对了，努力才有意义

📬 点个关注，下一个产品灵感可能就在下一篇。
```

```markdown
🔥 别等万事俱备，先搞起来再说

📬 关注我，看一个普通程序员怎么一步步搞到钱。
```

### 配图插入规则

1. **封面图**：放在标题下方
2. **章节插图**：放在对应章节标题下方
3. **信息图**：放在相关数据/概念描述之后
4. **图片路径**：使用相对路径 `./_attachments/xxx.png`

---

## 三、X (Twitter) Articles 版本

X Articles 支持两个语言版本：中文版和英文版。

### X Articles 写作核心原则

以下原则适用于所有 X Articles 版本（中文和英文）。这是从 280 字符帖子升级到长文写作的终极指南。

#### 1. 明确写作目的

**在写第一句之前，必须先回答这两个问题：**

- 读者读完后应该**想到**、**感受到**或**做什么**？
- 这篇文章**真正的目标读者**是谁？

明确的目的让你保持专注，让文字自然流淌。

#### 2. 标题和开头（Hook）

**好标题的三要素：** 具体、引发好奇、承诺价值。

| 差标题 ❌                              | 好标题 ✅                              |
| -------------------------------------- | -------------------------------------- |
| "2026年提高效率的技巧"                 | "为什么95%的效率建议都是废话"          |
| "Tips for Better Productivity in 2026" | "Why 95% of Productivity Advice Fails" |

**开头要求：**

- 用一个强有力的第一句抓住读者，引导他们进入你的故事
- 封面图同样关键，必须视觉吸引、与主题直接相关

#### 3. 为「扫读」而设计结构

大多数用户在手机上访问 X，会先扫读再决定是否细读。**让价值一眼就能看到：**

| 规则             | 说明                             |
| ---------------- | -------------------------------- |
| **短段落**       | 每段 2-4 行，绝不超过            |
| **密集小标题**   | 每 3-5 段落必须加一个小标题      |
| **列表优先**     | 用要点列表和编号列表，避免文字墙 |
| **加粗关键洞察** | 几乎每个章节都要加粗核心观点     |
| **一段一个想法** | 严格遵守：每段只讲一个观点       |

#### 4. 发展自然、可辨识的声音

无论是分析型、犀利型还是对话型，保持语气一致，让读者每次回来都感觉认识你。

**关键洞察：** 当写作变得太「专业」时，它通常也会变得无聊。**像和好朋友聊天一样写作**，而不是在讲堂上演讲。多用「你」和「你的」等对话式语言。

| 差写法 ❌                                         | 好写法 ✅                                                                                 |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| "成功人士总是会优先处理他们的任务"                | "你需要停止什么都做——专注于真正能推动结果的3件事"                                         |
| "Successful people always prioritize their tasks" | "You need to stop doing everything — focus on the 3 things that actually move the needle" |

#### 5. 展示，而不只是告诉

事实和数据很好，但**故事和例子才能让它们深入人心**。

**铁律：** 每提出一个观点，**立即**用证据支撑：

- 统计数据
- 个人故事
- 前后对比
- 嵌入你自己的 X 帖子或文章作为活生生的例子

#### 6. 无情地编辑

初稿是写给你自己的。第二稿（和第三稿）是写给读者的。

**写完后的编辑清单：**

- [ ] 删减 20-30% 的字数
- [ ] 移除填充词："very"、"really"、"in order to"、"非常"、"一定程度上"
- [ ] 大声朗读全文——别扭的句子会立刻跳出来

#### 7. 添加视觉和格式

图片、截图、图表，甚至嵌入的 X 帖子，都能打破文字块，让文章更易分享。

**规则：** 格式良好的文章（粗体标题、合理间距、配图）能获得**显著更高**的互动率。

#### 8. 有力地收尾

不要虎头蛇尾——**用能量收尾**，给读者一个收获或行动号召：

- 总结关键要点
- 提一个问题引发回复
- 鼓励分享或立即尝试一个建议

---

### X 推荐算法优化框架

> 基于 X 开源推荐算法代码仓库的分析，以下框架指导如何创作更容易获得推荐的 X Articles。

#### 核心原理：18 种互动预测

X 的 Phoenix 排名模型会预测每篇帖子触发 **18 种互动** 的概率，然后加权计算最终分数。理解这些信号是优化内容的关键。

#### 高权重正面信号（优先优化）

| 信号 | 描述 | 创作指导 |
|------|------|----------|
| **点赞 (favorite)** | ⭐⭐⭐⭐⭐ | 写能让读者产生「说得好」「深有同感」瞬间的金句 |
| **回复 (reply)** | ⭐⭐⭐⭐⭐ | 在结尾提出开放式问题，邀请读者分享观点或经历 |
| **转发 (retweet)** | ⭐⭐⭐⭐⭐ | 提供「社交货币」——让转发者显得有见识/有品味/有价值 |
| **引用 (quote)** | ⭐⭐⭐⭐ | 写有争议性或可延展的观点，激发读者「加评论转发」 |
| **私信分享 (share_via_dm)** | ⭐⭐⭐⭐ | 创造「这个你一定要看」的时刻——具体、实用、有启发 |
| **复制链接分享 (copy_link)** | ⭐⭐⭐ | 提供完整的价值，让读者愿意分享到其他平台 |
| **关注作者 (follow)** | ⭐⭐⭐⭐ | 在文中展示独特视角和持续价值，建立「还想看更多」的期待 |

#### 中权重互动信号

| 信号 | 描述 | 创作指导 |
|------|------|----------|
| **停留时间 (dwell)** | 用户在帖子上停留的时间 | 结构化内容，让读者愿意细读而非跳过 |
| **点击 (click)** | 通用帖子点击 | 标题和封面图要足够吸引人点进来 |
| **个人资料点击 (profile_click)** | 访问作者主页 | 文中自然展示专业性，激发「这人是谁」的好奇 |
| **视频观看 (video_view)** | 视频完整观看率 | 如有视频，确保前 3 秒抓住注意力 |
| **照片展开 (photo_expand)** | 点击查看完整图片 | 配图要有信息密度，让人想点开看清楚 |

#### 负面信号（必须避免）

| 信号 | 惩罚程度 | 触发原因 |
|------|----------|----------|
| **举报 (report)** | 🔻🔻🔻🔻🔻 | 内容违规、垃圾信息、误导性 |
| **屏蔽作者 (block)** | 🔻🔻🔻🔻🔻 | 内容令人反感、骚扰、低质量刷屏 |
| **静音作者 (mute)** | 🔻🔻🔻🔻 | 内容重复、过于频繁、不感兴趣 |
| **不感兴趣 (not_interested)** | 🔻🔻🔻 | 内容与用户兴趣不匹配 |

#### 算法友好型内容创作原则

**1. 为「分享」而写**

X 算法高度重视分享行为（特别是 DM 分享和复制链接）。每篇文章都要自问：

> 「读者会想把这篇发给谁？为什么？」

如果答不出具体的场景，内容可能缺乏分享驱动力。

**2. 激发回复和引用**

回复和引用是高权重信号。有效策略：

- 结尾提出开放式问题
- 留有「可补充」的空间
- 提出有争议但不极端的观点
- 邀请读者分享自己的经历

**3. 优化停留时间**

停留时间是重要的参与度信号：

- 使用小标题和列表，让扫读变成细读
- 每 3-5 段一个悬念或转折
- 数据、案例、故事交替，保持新鲜感
- 避免信息密度过低导致跳出

**4. 建立关注意愿**

「关注作者」是高价值信号，说明用户想要持续获取你的内容：

- 在文中自然展示独特视角
- 预告后续内容方向
- 在 CTA 中强调持续价值

**5. 网络内优先原则**

X 算法会优先推荐关注者的内容（网络内），再补充网络外发现。

- 对于已有粉丝：发布后立即与评论互动，激活网络内分发
- 对于新账号：重点优化「引用」和「分享」，借助网络外发现获取初始曝光

#### X Articles 优化检查清单

在发布前，对照以下清单检查：

**高权重信号优化：**

- [ ] 是否有至少 3 处能引发「说得好」瞬间的金句？（点赞优化）
- [ ] 结尾是否有开放式问题或讨论邀请？（回复优化）
- [ ] 内容是否具有「社交货币」属性——转发能让分享者显得有见识？（转发优化）
- [ ] 是否有可延展/有争议的观点激发引用？（引用优化）
- [ ] 是否有「这个你一定要看」的具体实用洞察？（私信分享优化）

**参与度优化：**

- [ ] 结构是否清晰，能让扫读变成细读？（停留时间优化）
- [ ] 标题和封面图是否足够吸引点击？（点击优化）
- [ ] 是否展示了独特视角，激发「这人是谁」的好奇？（个人资料点击优化）

**负面信号规避：**

- [ ] 内容是否真诚、有价值，不会被认为是垃圾信息？
- [ ] 观点是否有依据，不会被认为是误导性内容？
- [ ] 发布频率是否合理，不会让粉丝想静音？

---

### 3.1 中文版

#### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/x-cn.md
```

#### 结构规范

```markdown
# {文章标题}

{文章正文，包含配图}

---

### 关注我

如果这篇文章对你有帮助，欢迎关注我的 X 账号 **@rwayne**，我会持续分享产品开发、出海创业、AI 工具等内容。

👉 [Roland的思考日记](https://x.com/rwayne)
```

#### 中文版写作检查清单

**目的与受众：**

- [ ] 写作目的明确：读者读完后应该想到、感受到或做什么？
- [ ] 目标读者清晰：这篇文章真正写给谁？

**标题与开头：**

- [ ] 标题是否具体、引发好奇、承诺价值？
- [ ] 开头第一句是否能抓住读者并引导他们进入故事？
- [ ] 封面图是否视觉吸引、与主题相关？

**扫读友好结构：**

- [ ] 段落是否控制在 2-4 行（绝不超过）？
- [ ] 是否每 3-5 段有一个小标题？
- [ ] 是否用列表替代文字墙？
- [ ] 是否在几乎每个章节都加粗了核心观点？
- [ ] 是否每段只讲一个观点？

**声音与风格：**

- [ ] 是否像和好朋友聊天，而不是演讲？
- [ ] 是否多用「你」和「你的」等对话式语言？
- [ ] 语气是否一致（分析型/犀利型/对话型）？

**展示而非告知：**

- [ ] 是否为每个观点立即提供证据（数据、故事、对比）？
- [ ] 是否嵌入了自己的 X 帖子或文章作为例子？

**编辑：**

- [ ] 是否删减了 20-30% 的字数？
- [ ] 是否移除了填充词（「非常」「一定程度上」等）？
- [ ] 是否大声朗读过，确保句子流畅？

**收尾：**

- [ ] 结尾是否有力，包含总结/问题/行动号召？
- [ ] 是否避免了虎头蛇尾？

**格式：**

- [ ] 配图是否有效打破文字块？

---

### 3.2 英文版

#### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/x-en.md
```

#### 生成流程

1. **翻译**：将中文版 `x-cn.md` 翻译为英文
2. **保持结构**：保留原有的标题层级、配图位置
3. **替换 CTA**：使用英文版 CTA
4. **应用扫读优化**：确保英文版也符合上述写作原则

#### 结构规范

```markdown
# {English Title}

{Article content in English, with images}

---

### Follow Me

If you found this article helpful, follow me on X **@BuildWithJames** for more insights on product development, indie hacking, and AI tools.

👉 [Build With James](https://x.com/BuildWithJames)
```

#### 翻译原则

- 保持原文的语气和风格（conversational, engaging）
- 不要逐字翻译，而是传达相同的意思
- 保留技术术语的英文原名
- 调整表达方式适应英文读者习惯
- **禁止使用 em dash（—）**：使用逗号、句号或其他标点替代
- 使用 "you" 和 "your" 等对话式语言
- 移除填充词："very"、"really"、"in order to"、"actually" (除非用于强调)

#### 英文版写作检查清单

**Purpose & Audience:**

- [ ] Clear purpose: What should reader think/feel/do after reading?
- [ ] Target audience: Who is this actually for?

**Title & Hook:**

- [ ] Title: Is it specific, curiosity-sparking, and value-promising?
- [ ] Hook: Does the first sentence grab the reader and ease them into the story?
- [ ] Header image: Is it visually appealing and relevant?

**Structure for Skimmability:**

- [ ] Paragraphs: Are they 2-4 lines max?
- [ ] Subheadings: One every 3-5 paragraphs?
- [ ] Lists: Bullets/numbers instead of text walls?
- [ ] Bold: Is the key insight bolded in almost every section?
- [ ] One idea: Does each paragraph stick to one idea?

**Voice & Style:**

- [ ] Conversational: Sounds like talking to a friend, not lecturing?
- [ ] Using "you" and "your" throughout?
- [ ] Consistent tone: Analytical, spicy, or conversational?

**Show Don't Tell:**

- [ ] Evidence: Did you follow each claim with proof (stats, story, before/after)?
- [ ] Embedded examples: Any X posts or articles as living examples?

**Editing:**

- [ ] Cut 20-30% of word count?
- [ ] Removed filler phrases: "very", "really", "in order to"?
- [ ] Read aloud: Do all sentences flow naturally?

**Closing:**

- [ ] Ends with energy: Summary, question, or call to action?
- [ ] No fade out: Strong close instead of trailing off?

**Format:**

- [ ] No em dashes: Using commas or periods instead?
- [ ] Images and visuals: Breaking up text effectively?

---

## 四、LinkedIn 版本

### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/linkedin.md
```

### 生成流程

1. **基于英文版**：LinkedIn 版本基于英文版 X 文章生成
2. **替换 CTA**：将 X CTA 替换为 LinkedIn CTA
3. **封面图比例**：使用 1.86:1 比例的封面图
4. **禁止使用 em dash（—）**：使用逗号、句号或其他标点替代

### 结构规范

```markdown
# {English Title}

{Article content in English, with images}

---

### Connect With Me

If you enjoyed this article, let's connect on LinkedIn. I share insights on product development, indie hacking, and navigating the AI revolution.

👉 [James Gong on LinkedIn](https://www.linkedin.com/in/zifei/)

#IndieHacker #AI #Programming #ProductDevelopment #CareerAdvice
```

### 封面图规格

- **长宽比**：1.86:1
- **推荐尺寸**：1200 × 645 像素
- **文件名**：`cover-linkedin.png`

### 生成命令

```bash
# 生成 LinkedIn 版本（需要先有英文版 X 文章）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform linkedin

# 或者提供英文内容文件
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform linkedin --english-content output/{目录}/x-en.md
```

---

## 五、小红书长文版本

> **重要**：发布前请务必阅读 `references/xiaohongshu-compliance.md` 了解完整的社区规范要求。

### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/xhs-long.md
```

### 社区合规核心要求

**内容红线（绝对禁止）：**

- 涉军涉政、违禁物品、两性敏感、烟草、封建迷信、赌博
- 裸露或性暗示内容
- 站外引流（二维码、微信号、外链等）
- 盗用、抄袭、侵权内容

**用语规范（必须遵守）：**

- 禁止绝对化用语：最、第一、顶级、史上最、100%
- 禁止夸大功效：一分钟见效、吃完就变白
- 禁止诱导互动：双击有惊喜、评论抽奖

**内容风格（建议遵循）：**

- 真诚分享，避免虚假种草
- 积极正向，不贩卖焦虑
- 客观中立，不拉踩抹黑
- 实用有价值，通俗易懂

### 格式规范

**纯文本格式**（保存为 `.md` 但不使用 Markdown 语法），只支持以下排版：

- 换行（单个换行符）
- 分段（空行）
- 缩进（空格）
- 有序列表（1. 2. 3.）
- 无序列表（• 或 - ）
- 表情符号（如适用）

**禁止使用**：

- Markdown 语法（#、\*\*、[]() 等）
- 特殊符号过多
- 超链接

### 结构规范

```
{吸引眼球的开头，1-2 句，可用表情符号}

{正文第一部分}
{每段 3-5 行，空行分隔}

{正文第二部分}
{用通俗语言解释干货}

{正文第三部分}
{让读者有收获感}

{核心观点总结，1-2 句}

---

#标签1 #标签2 #标签3 #标签4 #标签5
```

### 改写原则

1. **精简内容**：将长文的字数保持在 800-1200 字以内
2. **口语化**：比原文更加口语化、轻松，像跟朋友聊天
3. **分段清晰**：每段 3-5 行，便于手机阅读
4. **金句突出**：保留或改写最有冲击力的金句
5. **开头吸睛**：第一句要能抓住注意力，引发好奇
6. **收获感**：用非常通俗易懂的语言整理成普通人能看懂、有收获的内容，保留里面的干货，并告诉普通人能从中学到什么

### 表情符号使用原则

- 可在开头、小标题、重点句后适当使用
- 不要过度使用，保持专业感
- 常用：💡 ✨ 🔥 📌 ⭐ 🎯 💪 🤔

### Hashtag 规则

- 不超过 5 个
- 与文章主题高度相关
- 符合所选人设
- 选择热门但不泛滥的标签
- 建议格式：`#标签` （井号后直接跟文字）

### 常用标签参考

| 主题          | 推荐标签                                          |
| ------------- | ------------------------------------------------- |
| 程序员/开发   | #程序员 #代码人生 #独立开发者 #技术人 #码农日常   |
| 副业/创业     | #副业 #搞钱 #创业 #被动收入 #自由职业             |
| AI/效率       | #AI工具 #效率提升 #工具推荐 #ChatGPT #人工智能    |
| 职场/成长     | #职场 #个人成长 #认知升级 #职业规划 #干货分享     |
| 出海          | #出海 #海外创业 #全球化 #跨境 #数字游民           |
| 妈妈/女性成长 | #妈妈成长 #女性力量 #认知升级 #读书笔记 #自我提升 |

---

## 六、小红书短文版本

> **重要**：发布前请务必阅读 `references/xiaohongshu-compliance.md` 了解完整的社区规范要求。

### 文件命名

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{日期}-{标题}/xhs-short.txt
```

### 社区合规核心要求

（同长文版本，详见上节或 `references/xiaohongshu-compliance.md`）

### 格式规范

**纯文本格式**，只支持以下排版：

- 换行（单个换行符）
- 分段（空行）
- 缩进（空格）
- 有序列表（1. 2. 3.）
- 无序列表（• 或 - ）

**禁止使用**：

- Markdown 语法（#、\*\*、[]() 等）
- 特殊符号过多
- 超链接

### 结构规范

```
{吸引眼球的开头，1-2 句}

{正文内容，改写精简至 500 字以内}

{核心观点总结，1-2 句}

---

#标签1 #标签2 #标签3 #标签4 #标签5
```

### 改写原则

1. **精简内容**：将长文的核心观点提炼至 500 字以内
2. **口语化**：比原文更加口语化、轻松
3. **分段清晰**：每段 3-5 行，便于手机阅读
4. **金句突出**：保留或改写最有冲击力的金句
5. **开头吸睛**：第一句要能抓住注意力

---

## 七、生成命令

### 一键生成所有平台版本（中文）

```bash
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md
```

### 一键生成所有平台版本（含英文版）

```bash
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform all-with-english
```

### 单独生成某平台版本

```bash
# 微信公众号
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform wechat

# X Articles（中文）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform x

# X Articles（英文）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform x-en

# LinkedIn（需要先有英文版 X 文章）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform linkedin

# 小红书长文（800-1200字）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform xiaohongshu-long

# 小红书短文（≤500字）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform xiaohongshu-short

# 小红书（两个版本都生成）
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --platform xiaohongshu
```

### 使用配图

如果用户上传了配图到 `_attachments/` 目录，脚本会自动检测并插入：

```bash
# 检查 _attachments 目录下的图片
ls /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/_attachments/
# cover-wechat.png, cover-x.png, cover-xhs.png, cover-linkedin.png, section-01.png, ...

# 生成时自动插入配图
python scripts/generate_platform_versions.py /Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{目录}/index.md --with-images
```

---

## 八、输出目录结构

生成完成后的目录结构：

```
/Users/rolandwong/Documents/Obsidian Vault/AI_Roland/01-内容生产/选题管理/02-待发布/{YYYY-MM-DD}-{文章标题}/
├── index.md                # 原始长文/元文章（纯文本）
├── promotion.md            # 传播素材
├── wechat.md               # 微信公众号版本
├── x-cn.md                 # X Articles 版本（中文）
├── x-en.md                 # X Articles 版本（英文）
├── linkedin.md             # LinkedIn 版本（英文）
├── xhs-long.md             # 小红书长文版本（800-1200字）
├── xhs-short.txt           # 小红书短文版本（≤500字）
├── xhs-preview.html        # 小红书 HTML 预览页
├── prompts.json            # 图片生成提示词
└── _attachments/           # Obsidian 附件目录
    ├── cover-wechat.png    # 封面图 (2.35:1)
    ├── cover-x.png         # 封面图 (3:1)
    ├── cover-xhs.png       # 封面图 (3:4)
    ├── cover-linkedin.png  # 封面图 (1.86:1)
    ├── section-01.png      # 章节插图
    ├── section-02.png
    ├── xhs-01.png          # 小红书截图
    ├── xhs-02.png
    └── ...
```

---

## 九、自检清单

### 微信公众号版本

- [ ] 头部关注引导是否添加？
- [ ] 配图是否正确插入？
- [ ] 作者介绍区块是否完整？
- [ ] 尾部互动文案是否添加？
- [ ] 格式是否符合 mdnice 规范？

### X Articles 版本（中文）

- [ ] 文章标题是否使用 H1？
- [ ] 配图路径是否正确？
- [ ] 尾部 CTA 是否包含 @rwayne？
- [ ] 链接是否正确指向 https://x.com/rwayne？

### X Articles 版本（英文）

- [ ] 是否基于中文版翻译？
- [ ] 翻译是否自然流畅？
- [ ] 尾部 CTA 是否包含 @BuildWithJames？
- [ ] 链接是否正确指向 https://x.com/BuildWithJames？
- [ ] 封面图是否使用 3:1 比例？

### LinkedIn 版本

- [ ] 是否基于英文版 X 文章？
- [ ] CTA 是否指向 LinkedIn 账号？
- [ ] 链接是否正确指向 https://www.linkedin.com/in/zifei/？
- [ ] 封面图是否使用 1.86:1 比例？
- [ ] 文章末尾是否包含不超过 5 个 hashtag？

### 小红书长文版本（xhs-long.md）

**基础格式：**

- [ ] 字数是否在 800-1200 字之间？
- [ ] 是否为纯文本格式（不使用 Markdown 语法）？
- [ ] 是否比原文更口语化、轻松？
- [ ] 每段是否控制在 3-5 行？
- [ ] 是否保留了核心金句？
- [ ] 开头是否足够吸引人？
- [ ] 内容是否通俗易懂、有收获感？
- [ ] Hashtag 是否不超过 5 个？
- [ ] Hashtag 是否符合所选人设？
- [ ] 表情符号是否适当使用（不过度）？

**社区合规检查：**

- [ ] 不含绝对化用语（最、第一、顶级、史上最、100%等）？
- [ ] 不夸大功效或效果承诺？
- [ ] 不含诱导关注/点赞/评论的内容？
- [ ] 不含站外引流信息（二维码、微信号、外链等）？
- [ ] 不贩卖焦虑、不挑起对立？
- [ ] 内容原创或已获授权？
- [ ] 如有利益相关已明确标注？

### 小红书短文版本（xhs-short.txt）

**基础格式：**

- [ ] 字数是否在 500 字以内？
- [ ] 是否为纯文本格式？
- [ ] 是否去除了所有 Markdown 语法？
- [ ] Hashtag 是否不超过 5 个？
- [ ] 开头是否足够吸引人？

**社区合规检查：**

- [ ] 不含绝对化用语？
- [ ] 不夸大功效或效果承诺？
- [ ] 不含诱导互动内容？
- [ ] 不含站外引流信息？
- [ ] 内容原创或已获授权？

### 小红书图片合规（封面图及内容图）

- [ ] 无其他平台水印或 logo？
- [ ] 无二维码或联系方式？
- [ ] 画风符合小红书社区调性（清新、真实、美好）？
- [ ] 无低俗、猎奇、暴力恐怖元素？
- [ ] 无裸露或性暗示内容？
- [ ] 素材原创或已获授权（无未授权的明星/IP）？
- [ ] 封面图文字不超过图片面积 20%？
- [ ] 信息图中的数据/内容准确可查？

---

## 十、一键发布到平台

文章生成完成后，可以使用以下 skills 直接发布到对应平台：

### 发布到 X Articles

```
/x-article-publisher
```

- 来源：https://github.com/wshuyi/x-article-publisher-skill
- 功能：将 Markdown 文章发布到 X Articles 编辑器，自动处理格式转换和封面图上传

### 发布到 LinkedIn Articles

```
/linkedin-article-publisher
```

- 来源：https://github.com/iamzifei/linkedin-article-publisher-skill
- 功能：将 Markdown 文章发布到 LinkedIn Articles 编辑器，自动处理格式转换和封面图上传

### 使用流程

1. 确保已生成目标平台的文章版本（如 `x-cn.md` 或 `linkedin.md`）
2. 确保封面图已生成（如 `cover-x.png` 或 `cover-linkedin.png`）
3. 调用对应的发布 skill
4. 按 skill 指引完成发布
