# 引擎1 配置系统

> 仅 Roland 可修改，客户使用预设版本

## 文件结构

```
config/
├── presets.json    # 预设销售版本（定义完整包）
├── stages.json     # 流水线阶段配置
└── platforms.json  # 发布平台配置
```

## 预设版本 (presets.json)

定义可售卖的完整包版本，每个版本包含：
- `stages` - 开启哪些阶段
- `platforms` - 包含哪些平台
- `brands` - 用哪些品牌
- `skills` - 开启哪些子技能

### 当前预设

| 版本 | 阶段 | 平台 | 品牌 |
|------|------|------|------|
| 留学专家版 | 全部4阶段 | 公众号+X+LinkedIn | roland-wayne |
| 健康布道版 | 全部4阶段 | X+LinkedIn | roland-med |
| 商业IP版 | 全部4阶段 | 公众号+X+小红书+LinkedIn | dankoe |
| 基础版 | 筛选+创作+保存 | 公众号 | 无品牌 |

## 修改预设

1. 编辑 `presets.json`
2. 修改 `activePreset` 为目标版本
3. 或创建新预设

## 交付流程

1. 选一个预设版本
2. 根据预设配置，生成对应的完整包
3. 交付给客户