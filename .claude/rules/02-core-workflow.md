<!--
  AI Second Brain System
  Copyright (c) 2026 Roland Wayne (https://rolandwayne.com)

  This file is part of the AI Second Brain System.
  Licensed under Dual License: AGPL-3.0 (Personal) / Commercial (Business)

  Personal Use: Free under AGPL-3.0
  Commercial Use: Requires license from Roland Wayne

  Unauthorized commercial use is prohibited.
  See LICENSE file for complete terms.
-->

# 核心工作流规范

**主动搜索优先**：问用户前必须先用 Glob/Grep/Read 搜索现有文件。

**二进制文件**：`.docx` → `textutil -convert txt <file>`；`.xlsx` → python3+pandas/openpyxl。禁止直接 Read。

**指令遵循度**：每次回复开头用 `✓`；没有 `✓` 说明上下文过载，提醒用户 /clear。

**Plan Mode**：非简单任务前 Shift+Tab 两次进入。

**卡住时**：/clear 重开 → 拆小步骤 → 写最小示例 → 换角度描述。

**会话总结**：用户说"总结"/"保存会话"/"done"/"/done"/"会话总结" → 立即保存会话摘要。

**决策确认**：架构决策/影响现有系统/多方案选择/删除重构 → 必须询问用户。

**需求驱动，禁止惯性假设**：方案必须从用户的实际需求出发，不从现有基础设施反推。

**代码质量**：禁止兼容性代码/if 分支修复/不必要错误处理/过度抽象。

**进度模式**（`/进度`）：分阶段报告（扫描→分析→执行→收尾），每阶段用真实计数。

**输出规范**：禁止编号列表（除非明确要求），独白式格式。

**内容生产路径**：内容生成任务必须保存到用户已建立的内容目录。

**多步骤工作流确认**：多步骤工作流必须等待用户明确确认再进入下一阶段。

**内容评分标准**：生成带分数/评级的内容时，9.0 以下视为需要改进，不是批准通过。
