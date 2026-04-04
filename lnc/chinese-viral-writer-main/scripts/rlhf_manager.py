#!/usr/bin/env python3
"""
RLHF Loop 自进化系统管理器

自动化管理规则库、记录 Episode、计算得分、触发整合。

用法:
    python scripts/rlhf_manager.py init                    # 初始化规则库
    python scripts/rlhf_manager.py start-episode           # 开始新 episode
    python scripts/rlhf_manager.py apply-rules             # 获取本次应用的规则
    python scripts/rlhf_manager.py record-feedback         # 记录反馈
    python scripts/rlhf_manager.py update-scores           # 更新规则得分
    python scripts/rlhf_manager.py consolidate             # 整合规则
    python scripts/rlhf_manager.py report                  # 输出进化报告
    python scripts/rlhf_manager.py export                  # 导出规则
    python scripts/rlhf_manager.py reset                   # 重置进化状态
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
import random
import uuid

# 尝试导入 yaml，如果没有安装则使用简单的解析
try:
    import yaml
except ImportError:
    yaml = None


class SimpleYAML:
    """简单的 YAML 解析器（无依赖）"""

    @staticmethod
    def load(content: str) -> dict:
        """简单的 YAML 解析"""
        result = {}
        current_key = None
        current_list = None
        indent_stack = [(0, result)]

        lines = content.split('\n')
        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                continue

            # 计算缩进
            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            # 处理列表项
            if stripped.startswith('- '):
                value = stripped[2:]
                if ':' in value and not value.startswith('"'):
                    # 字典项
                    key, val = value.split(':', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if current_list is not None:
                        if not current_list:
                            current_list.append({key: val})
                        else:
                            current_list[-1][key] = val
                else:
                    if current_list is not None:
                        current_list.append(value)
                continue

            # 处理键值对
            if ':' in stripped:
                key, value = stripped.split(':', 1)
                key = key.strip()
                value = value.strip()

                if value == '' or value == '[]':
                    # 空值或空列表
                    result[key] = [] if value == '[]' else None
                    current_list = result[key] if value == '[]' else None
                    current_key = key
                elif value.lower() in ('null', 'none'):
                    result[key] = None
                elif value.lower() == 'true':
                    result[key] = True
                elif value.lower() == 'false':
                    result[key] = False
                elif value.isdigit():
                    result[key] = int(value)
                elif value.replace('.', '').isdigit():
                    result[key] = float(value)
                else:
                    result[key] = value.strip('"').strip("'")

        return result

    @staticmethod
    def dump(data: dict) -> str:
        """简单的 YAML 序列化"""
        def serialize(obj, indent=0):
            lines = []
            prefix = '  ' * indent

            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (dict, list)) and value:
                        lines.append(f"{prefix}{key}:")
                        lines.extend(serialize(value, indent + 1))
                    elif isinstance(value, list) and not value:
                        lines.append(f"{prefix}{key}: []")
                    elif value is None:
                        lines.append(f"{prefix}{key}: null")
                    elif isinstance(value, bool):
                        lines.append(f"{prefix}{key}: {str(value).lower()}")
                    elif isinstance(value, str):
                        if ':' in value or '#' in value:
                            lines.append(f'{prefix}{key}: "{value}"')
                        else:
                            lines.append(f"{prefix}{key}: {value}")
                    else:
                        lines.append(f"{prefix}{key}: {value}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        first = True
                        for key, value in item.items():
                            if first:
                                lines.append(f"{prefix}- {key}: {value}")
                                first = False
                            else:
                                lines.append(f"{prefix}  {key}: {value}")
                    else:
                        lines.append(f"{prefix}- {item}")

            return lines

        return '\n'.join(serialize(data))


class RLHFManager:
    """RLHF 循环管理器"""

    # 默认规则库（从 methodology.md 和 style-rules.md 提取）
    DEFAULT_RULES = [
        {
            "id": "rule_001",
            "category": "张力场",
            "content": "寻找宏大叙事与个体真实之间的张力",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_002",
            "category": "众生相",
            "content": "使用群体标签+日常场景+真实行为构建众生相",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_003",
            "category": "情绪扳机",
            "content": "情绪扳机要用总结性概括加带情绪的断言",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_004",
            "category": "时效性",
            "content": "嫁接当下热点词汇增加时效性",
            "priority": "medium",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_005",
            "category": "叙事",
            "content": "必须使用第一人称「我」叙事",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_006",
            "category": "语气",
            "content": "口语化表达，像和朋友深夜聊天",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_007",
            "category": "结构",
            "content": "跳跃式思维，避免首先其次的线性结构",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_008",
            "category": "节奏",
            "content": "短句为主，几句话就分段",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_009",
            "category": "引导",
            "content": "多用设问引导读者思考",
            "priority": "medium",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_010",
            "category": "金句",
            "content": "金句要够狠，能让读者截图发朋友圈",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_011",
            "category": "禁区",
            "content": "禁止使用破折号、冒号、双引号",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_012",
            "category": "禁区",
            "content": "禁止使用首先、其次、此外、总而言之",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_013",
            "category": "禁区",
            "content": "禁止使用任何 Emoji",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_014",
            "category": "禁区",
            "content": "禁止学术腔和说教腔",
            "priority": "high",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
        {
            "id": "rule_015",
            "category": "排版",
            "content": "段落之间空一行，一段3-5行以内",
            "priority": "medium",
            "score": 0.5,
            "confidence": 0.0,
            "applied_count": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "neutral": 0,
        },
    ]

    def __init__(self, state_file: Optional[str] = None):
        """初始化管理器"""
        self.script_dir = Path(__file__).parent.parent

        # 确定状态文件位置
        if state_file:
            self.state_file = Path(state_file)
        else:
            # 优先使用用户工作目录
            user_state = Path.cwd() / '.viral-writer-evolution.yaml'
            default_state = self.script_dir / 'references' / 'evolution-state.yaml'

            if user_state.exists():
                self.state_file = user_state
            else:
                self.state_file = default_state

        self.state = self._load_state()

    def _load_state(self) -> dict:
        """加载进化状态"""
        if not self.state_file.exists():
            return self._create_initial_state()

        content = self.state_file.read_text(encoding='utf-8')

        if yaml:
            return yaml.safe_load(content) or self._create_initial_state()
        else:
            return SimpleYAML.load(content) or self._create_initial_state()

    def _save_state(self):
        """保存进化状态"""
        if yaml:
            content = yaml.dump(self.state, allow_unicode=True, default_flow_style=False, sort_keys=False)
        else:
            content = SimpleYAML.dump(self.state)

        self.state_file.write_text(content, encoding='utf-8')

    def _create_initial_state(self) -> dict:
        """创建初始状态"""
        return {
            'meta': {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_episodes': 0,
                'consolidation_count': 0,
                'next_consolidation_at': 10,
                'cold_start': True,
            },
            'rules': [],
            'episodes': [],
            'pending_validation': [],
            'pending_removal': [],
            'exploration_queue': [],
            'ab_tests': [],
            'current_episode': None,
        }

    def init(self, force: bool = False):
        """初始化规则库"""
        if self.state.get('rules') and not force:
            print("规则库已存在。使用 --force 强制重新初始化。")
            return

        now = datetime.now().isoformat()

        # 初始化规则
        rules = []
        for rule_template in self.DEFAULT_RULES:
            rule = rule_template.copy()
            rule['created_at'] = now
            rule['last_applied'] = None
            rule['parent_rule'] = None
            rule['child_rules'] = []
            rule['conditions'] = []
            rule['examples'] = {'good': [], 'bad': []}
            rules.append(rule)

        self.state['rules'] = rules
        self.state['meta']['created_at'] = now
        self.state['meta']['last_updated'] = now
        self.state['meta']['cold_start'] = True

        self._save_state()
        print(f"已初始化 {len(rules)} 条默认规则。")
        print(f"状态文件保存在: {self.state_file}")

    def start_episode(self, mode: str = '原创', topic: str = '') -> dict:
        """开始新的 episode"""
        episode_id = f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

        # 选择本次应用的规则
        applied_rules = self._select_rules()

        episode = {
            'episode_id': episode_id,
            'date': datetime.now().isoformat(),
            'mode': mode,
            'topic': topic,
            'rules_applied': [r['id'] for r in applied_rules],
            'output_version': 1,
            'revisions': 0,
            'final_adopted': None,
            'explicit_feedback': [],
            'implicit_signals': {
                'revision_count': 0,
                'adopted': False,
            },
            'status': 'in_progress',
        }

        self.state['current_episode'] = episode
        self.state['meta']['last_updated'] = datetime.now().isoformat()
        self._save_state()

        # 输出应用的规则
        print(f"\n=== Episode 开始: {episode_id} ===")
        print(f"模式: {mode}")
        print(f"主题: {topic}")
        print(f"\n本次应用的规则 ({len(applied_rules)} 条):")
        for rule in applied_rules:
            score_str = f"[{rule['score']:.2f}]" if rule['confidence'] > 0 else "[?]"
            print(f"  {score_str} {rule['id']}: {rule['content']}")

        return episode

    def _select_rules(self) -> list:
        """选择本次应用的规则"""
        rules = self.state.get('rules', [])
        if not rules:
            return []

        total_episodes = self.state['meta'].get('total_episodes', 0)

        # 每 5 次进行一次探索
        explore_mode = (total_episodes + 1) % 5 == 0

        selected = []

        # 高分高置信规则（优先选择）
        high_score_rules = [r for r in rules if r.get('score', 0.5) > 0.7 and r.get('confidence', 0) > 0.8]

        # 中等规则
        medium_rules = [r for r in rules if 0.3 <= r.get('score', 0.5) <= 0.7]

        # 低置信规则（探索用）
        low_confidence_rules = [r for r in rules if r.get('confidence', 0) < 0.5]

        # 必选规则（priority=high 且没有负面记录）
        must_have = [r for r in rules if r.get('priority') == 'high' and r.get('score', 0.5) >= 0.3]
        selected.extend(must_have)

        # 如果是探索模式，额外添加低置信规则
        if explore_mode and low_confidence_rules:
            explore_rule = random.choice(low_confidence_rules)
            if explore_rule not in selected:
                selected.append(explore_rule)
                print(f"\n[探索模式] 尝试低置信规则: {explore_rule['id']}")

        # 添加一些中等规则
        remaining = [r for r in medium_rules if r not in selected]
        if remaining:
            selected.extend(random.sample(remaining, min(3, len(remaining))))

        return selected

    def apply_rules(self) -> list:
        """获取本次应用的规则（供 Claude 读取）"""
        episode = self.state.get('current_episode')
        if not episode:
            print("没有进行中的 episode，请先执行 start-episode")
            return []

        rule_ids = episode.get('rules_applied', [])
        rules = self.state.get('rules', [])

        applied = [r for r in rules if r['id'] in rule_ids]

        # 输出 JSON 格式，便于 Claude 解析
        print(json.dumps(applied, ensure_ascii=False, indent=2))
        return applied

    def record_feedback(self, rule_id: str, signal: float, comment: str = ''):
        """记录对特定规则的反馈

        signal 值:
            +1.0 = 明确表扬
            +0.5 = 无修改直接采用
            +0.0 = 有小修改
            -0.5 = 大幅修改
            -1.0 = 明确批评
        """
        episode = self.state.get('current_episode')
        if not episode:
            print("没有进行中的 episode")
            return

        feedback = {
            'rule_id': rule_id,
            'signal': signal,
            'comment': comment,
            'timestamp': datetime.now().isoformat(),
        }

        episode['explicit_feedback'].append(feedback)
        self._save_state()

        signal_desc = {1.0: '表扬', 0.5: '采用', 0.0: '小改', -0.5: '大改', -1.0: '批评'}
        print(f"已记录反馈: {rule_id} -> {signal_desc.get(signal, signal)}")

    def record_revision(self):
        """记录一次修改"""
        episode = self.state.get('current_episode')
        if not episode:
            print("没有进行中的 episode")
            return

        episode['revisions'] += 1
        episode['implicit_signals']['revision_count'] += 1
        self._save_state()
        print(f"修改次数: {episode['revisions']}")

    def complete_episode(self, adopted: bool = True):
        """完成当前 episode"""
        episode = self.state.get('current_episode')
        if not episode:
            print("没有进行中的 episode")
            return

        episode['final_adopted'] = adopted
        episode['implicit_signals']['adopted'] = adopted
        episode['status'] = 'completed'

        # 添加到历史记录
        if 'episodes' not in self.state:
            self.state['episodes'] = []
        self.state['episodes'].append(episode)

        # 更新元数据
        self.state['meta']['total_episodes'] = len(self.state['episodes'])
        self.state['meta']['last_updated'] = datetime.now().isoformat()

        # 清空当前 episode
        self.state['current_episode'] = None

        self._save_state()

        print(f"\n=== Episode 完成: {episode['episode_id']} ===")
        print(f"采用: {'是' if adopted else '否'}")
        print(f"修改次数: {episode['revisions']}")
        print(f"总 Episode 数: {self.state['meta']['total_episodes']}")

        # 自动更新得分
        self.update_scores()

        # 检查是否需要整合
        if self.state['meta']['total_episodes'] >= self.state['meta'].get('next_consolidation_at', 10):
            print("\n[提醒] 已达到整合触发点，建议执行 consolidate 命令")

    def update_scores(self):
        """根据反馈更新规则得分"""
        episodes = self.state.get('episodes', [])
        rules = self.state.get('rules', [])

        if not rules:
            print("没有规则需要更新")
            return

        # 重新计算每条规则的得分
        for rule in rules:
            rule_id = rule['id']

            # 收集所有关于这条规则的反馈
            feedbacks = []
            implicit_signals = []

            for episode in episodes:
                if rule_id in episode.get('rules_applied', []):
                    # 显式反馈
                    for fb in episode.get('explicit_feedback', []):
                        if fb.get('rule_id') == rule_id:
                            feedbacks.append(fb['signal'])

                    # 隐式信号
                    adopted = episode.get('implicit_signals', {}).get('adopted', False)
                    revisions = episode.get('implicit_signals', {}).get('revision_count', 0)

                    if adopted and revisions == 0:
                        implicit_signals.append(0.5)  # 无修改采用
                    elif adopted and revisions <= 2:
                        implicit_signals.append(0.0)  # 小修改
                    elif adopted and revisions > 2:
                        implicit_signals.append(-0.5)  # 大修改
                    elif not adopted:
                        implicit_signals.append(-0.5)

            # 计算得分
            all_signals = feedbacks + implicit_signals
            applied_count = len([e for e in episodes if rule_id in e.get('rules_applied', [])])

            if all_signals:
                score = sum(all_signals) / len(all_signals)
                # 归一化到 0-1
                score = (score + 1) / 2
                rule['score'] = round(max(0, min(1, score)), 2)

            rule['applied_count'] = applied_count

            # 计算置信度
            if applied_count > 0:
                rule['confidence'] = round(1 - 1 / (applied_count + 1), 2)

            # 统计正负反馈
            rule['positive_feedback'] = len([s for s in all_signals if s > 0])
            rule['negative_feedback'] = len([s for s in all_signals if s < 0])
            rule['neutral'] = len([s for s in all_signals if s == 0])

            if applied_count > 0:
                rule['last_applied'] = max(
                    e['date'] for e in episodes if rule_id in e.get('rules_applied', [])
                )

        # 检查冷启动状态
        total_episodes = len(episodes)
        if total_episodes >= 5:
            self.state['meta']['cold_start'] = False

        self._save_state()
        print(f"已更新 {len(rules)} 条规则的得分")

    def consolidate(self):
        """整合规则"""
        rules = self.state.get('rules', [])

        if not rules:
            print("没有规则需要整合")
            return

        print("\n=== 规则整合 ===\n")

        # 1. 识别高分规则
        high_score = [r for r in rules if r.get('score', 0.5) > 0.7 and r.get('confidence', 0) > 0.8]
        print(f"高分规则 (>0.7, 置信度>80%): {len(high_score)} 条")
        for r in high_score:
            print(f"  [强化] {r['id']}: {r['content']} (得分: {r['score']}, 置信度: {r['confidence']})")

        # 2. 识别低分规则（待淘汰）
        low_score = [r for r in rules if r.get('score', 0.5) < 0.3 and r.get('confidence', 0) > 0.8]
        print(f"\n低分规则 (<0.3, 置信度>80%): {len(low_score)} 条")
        for r in low_score:
            print(f"  [待淘汰] {r['id']}: {r['content']} (得分: {r['score']})")
            # 添加到待淘汰队列
            if r['id'] not in [x['id'] for x in self.state.get('pending_removal', [])]:
                if 'pending_removal' not in self.state:
                    self.state['pending_removal'] = []
                self.state['pending_removal'].append({
                    'id': r['id'],
                    'content': r['content'],
                    'score': r['score'],
                    'added_at': datetime.now().isoformat(),
                })

        # 3. 识别低置信规则（需要更多数据）
        low_confidence = [r for r in rules if r.get('confidence', 0) < 0.5]
        print(f"\n低置信规则 (置信度<50%): {len(low_confidence)} 条")
        for r in low_confidence:
            print(f"  [待验证] {r['id']}: {r['content']} (应用次数: {r.get('applied_count', 0)})")

        # 4. 识别死规则（长期未使用）
        now = datetime.now()
        dead_rules = []
        for r in rules:
            if r.get('last_applied'):
                try:
                    last_applied = datetime.fromisoformat(r['last_applied'].replace('Z', '+00:00'))
                    days_since = (now - last_applied.replace(tzinfo=None)).days
                    if days_since > 30 and r.get('applied_count', 0) < 3:
                        dead_rules.append((r, days_since))
                except:
                    pass

        if dead_rules:
            print(f"\n死规则 (>30天未使用): {len(dead_rules)} 条")
            for r, days in dead_rules:
                print(f"  [清理] {r['id']}: {r['content']} ({days}天未使用)")

        # 更新整合计数
        self.state['meta']['consolidation_count'] = self.state['meta'].get('consolidation_count', 0) + 1
        self.state['meta']['next_consolidation_at'] = self.state['meta']['total_episodes'] + 10
        self.state['meta']['last_updated'] = datetime.now().isoformat()

        self._save_state()

        print(f"\n整合完成。下次整合触发点: Episode #{self.state['meta']['next_consolidation_at']}")

    def report(self):
        """输出进化报告"""
        meta = self.state.get('meta', {})
        rules = self.state.get('rules', [])
        episodes = self.state.get('episodes', [])

        print("\n" + "=" * 50)
        print("         Skill 进化报告")
        print("=" * 50)

        # 基本统计
        print(f"\n总创作次数: {meta.get('total_episodes', 0)}")
        print(f"整合次数: {meta.get('consolidation_count', 0)}")
        print(f"冷启动: {'是' if meta.get('cold_start', True) else '否'}")

        if episodes:
            # 计算平均修改轮次
            avg_revisions = sum(e.get('revisions', 0) for e in episodes) / len(episodes)
            # 计算采用率
            adopted_count = len([e for e in episodes if e.get('final_adopted', False)])
            adoption_rate = adopted_count / len(episodes) * 100

            print(f"平均修改轮次: {avg_revisions:.1f}")
            print(f"采用率: {adoption_rate:.0f}%")

        # 高分规则
        high_score = sorted(
            [r for r in rules if r.get('confidence', 0) > 0.5],
            key=lambda x: x.get('score', 0),
            reverse=True
        )[:5]

        if high_score:
            print("\n### 高分规则 TOP 5")
            for i, r in enumerate(high_score, 1):
                print(f"  {i}. [{r['score']:.2f}] {r['content']}")

        # 低分规则
        low_score = [r for r in rules if r.get('score', 0.5) < 0.3 and r.get('confidence', 0) > 0.5]
        if low_score:
            print("\n### 低分规则（待淘汰）")
            for r in low_score:
                print(f"  [{r['score']:.2f}] {r['content']} <- 建议删除")

        # 待验证规则
        low_conf = [r for r in rules if r.get('confidence', 0) < 0.5 and r.get('applied_count', 0) > 0]
        if low_conf:
            print("\n### 待验证规则（低置信度）")
            for r in low_conf:
                print(f"  [?] {r['content']} (仅应用 {r.get('applied_count', 0)} 次)")

        # 建议操作
        print("\n### 建议操作")
        suggestions = []

        if low_score:
            suggestions.append(f"- 删除 {len(low_score)} 条低分规则")
        if meta.get('total_episodes', 0) >= meta.get('next_consolidation_at', 10):
            suggestions.append("- 执行规则整合 (consolidate)")
        if meta.get('cold_start', True) and meta.get('total_episodes', 0) < 5:
            suggestions.append(f"- 继续收集反馈 (还需 {5 - meta.get('total_episodes', 0)} 次)")

        if suggestions:
            for s in suggestions:
                print(s)
        else:
            print("- 暂无")

        print("\n" + "=" * 50)

    def export_rules(self, output_file: Optional[str] = None):
        """导出规则库"""
        rules = self.state.get('rules', [])

        # 只导出核心字段
        exported = []
        for r in rules:
            exported.append({
                'id': r['id'],
                'category': r.get('category', ''),
                'content': r['content'],
                'priority': r.get('priority', 'medium'),
                'score': r.get('score', 0.5),
                'confidence': r.get('confidence', 0),
            })

        output = json.dumps(exported, ensure_ascii=False, indent=2)

        if output_file:
            Path(output_file).write_text(output, encoding='utf-8')
            print(f"规则已导出到: {output_file}")
        else:
            print(output)

    def reset(self, confirm: bool = False):
        """重置进化状态"""
        if not confirm:
            print("警告: 这将清空所有学习记录！")
            print("使用 --confirm 确认重置")
            return

        self.state = self._create_initial_state()
        self._save_state()
        print("已重置进化状态。请执行 init 重新初始化规则库。")

    def add_rule(self, category: str, content: str, priority: str = 'medium'):
        """添加新规则"""
        rules = self.state.get('rules', [])

        # 生成新 ID
        existing_ids = [r['id'] for r in rules]
        new_id = f"rule_{len(rules) + 1:03d}"
        while new_id in existing_ids:
            new_id = f"rule_{int(new_id.split('_')[1]) + 1:03d}"

        new_rule = {
            'id': new_id,
            'category': category,
            'content': content,
            'priority': priority,
            'score': 0.5,
            'confidence': 0.0,
            'applied_count': 0,
            'positive_feedback': 0,
            'negative_feedback': 0,
            'neutral': 0,
            'created_at': datetime.now().isoformat(),
            'last_applied': None,
            'parent_rule': None,
            'child_rules': [],
            'conditions': [],
            'examples': {'good': [], 'bad': []},
        }

        rules.append(new_rule)
        self.state['rules'] = rules
        self._save_state()

        print(f"已添加规则: {new_id} - {content}")

    def remove_rule(self, rule_id: str):
        """删除规则"""
        rules = self.state.get('rules', [])
        original_count = len(rules)

        rules = [r for r in rules if r['id'] != rule_id]

        if len(rules) < original_count:
            self.state['rules'] = rules
            self._save_state()
            print(f"已删除规则: {rule_id}")
        else:
            print(f"未找到规则: {rule_id}")

    def list_articles(self) -> list:
        """扫描并列出所有历史文章（仅 articles 目录下的元文章）"""
        articles = []

        # 只扫描 articles 目录（output 目录是平台变体，不需要单独记录反馈）
        articles_dir = self.script_dir / 'articles'

        if not articles_dir.exists():
            print(f"articles 目录不存在: {articles_dir}")
            return articles

        # 扫描 .md 文件
        for md_file in articles_dir.rglob('*.md'):
            # 跳过非文章文件
            if md_file.name in ['README.md', 'SKILL.md', 'promotion.md']:
                continue

            # 提取文章信息
            try:
                content = md_file.read_text(encoding='utf-8')
                lines = content.strip().split('\n')

                # 提取标题
                title = md_file.stem
                for line in lines[:10]:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break

                # 从文件名提取日期（格式：2026-01-01-title.md 或 2026-title.md）
                date_str = None
                stem = md_file.stem
                # 尝试 YYYY-MM-DD 格式
                if len(stem) >= 10 and stem[4] == '-' and stem[7] == '-':
                    try:
                        date_str = stem[:10]
                        datetime.strptime(date_str, '%Y-%m-%d')
                    except:
                        date_str = None
                # 尝试 YYYY 格式
                if not date_str and len(stem) >= 4 and stem[:4].isdigit():
                    date_str = f"{stem[:4]}-01-01"

                # 检查是否已导入
                episodes = self.state.get('episodes', [])
                already_imported = any(
                    e.get('article_path') == str(md_file) for e in episodes
                )

                articles.append({
                    'path': str(md_file),
                    'title': title,
                    'date': date_str,
                    'word_count': len(content),
                    'imported': already_imported,
                })
            except Exception as e:
                print(f"警告: 无法读取 {md_file}: {e}")

        # 按日期排序
        articles.sort(key=lambda x: x.get('date') or '0000-00-00', reverse=True)

        # 输出列表
        print(f"\n找到 {len(articles)} 篇文章:\n")
        for i, article in enumerate(articles, 1):
            status = "[已导入]" if article['imported'] else "[待导入]"
            date = article['date'] or '未知日期'
            print(f"  {i}. {status} {date} - {article['title']}")
            print(f"     路径: {article['path']}")

        return articles

    def import_episode(self, article_path: str, mode: str = '原创',
                       adopted: bool = True, revisions: int = 0):
        """导入历史文章作为 episode"""
        path = Path(article_path)

        if not path.exists():
            print(f"文件不存在: {article_path}")
            return None

        # 检查是否已导入
        episodes = self.state.get('episodes', [])
        for ep in episodes:
            if ep.get('article_path') == str(path):
                print(f"文章已导入: {ep['episode_id']}")
                print("使用 record-feedback 命令添加反馈")
                return ep

        # 读取文章
        content = path.read_text(encoding='utf-8')
        lines = content.strip().split('\n')

        # 提取标题
        title = path.stem
        for line in lines[:10]:
            if line.startswith('# '):
                title = line[2:].strip()
                break

        # 尝试从目录名提取日期
        date_str = None
        parent_name = path.parent.name
        if parent_name and len(parent_name) >= 10:
            try:
                date_str = parent_name[:10]
                datetime.strptime(date_str, '%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')

        # 创建 episode
        episode_id = f"ep_{date_str.replace('-', '')}_{uuid.uuid4().hex[:6]}"

        # 假设所有规则都被应用（因为是历史文章）
        all_rule_ids = [r['id'] for r in self.state.get('rules', [])]

        episode = {
            'episode_id': episode_id,
            'date': f"{date_str}T00:00:00",
            'mode': mode,
            'topic': title,
            'article_path': str(path),
            'rules_applied': all_rule_ids,
            'output_version': 1,
            'revisions': revisions,
            'final_adopted': adopted,
            'explicit_feedback': [],
            'implicit_signals': {
                'revision_count': revisions,
                'adopted': adopted,
            },
            'status': 'imported',
        }

        # 添加到历史
        if 'episodes' not in self.state:
            self.state['episodes'] = []
        self.state['episodes'].append(episode)

        # 更新元数据
        self.state['meta']['total_episodes'] = len(self.state['episodes'])
        self.state['meta']['last_updated'] = datetime.now().isoformat()

        # 设置为当前 episode 以便记录反馈
        self.state['current_episode'] = episode

        self._save_state()

        print(f"\n=== 已导入文章: {episode_id} ===")
        print(f"标题: {title}")
        print(f"日期: {date_str}")
        print(f"路径: {path}")
        print(f"\n现在可以使用以下命令记录反馈:")
        print(f"  python scripts/rlhf_manager.py record-feedback <rule_id> <signal>")
        print(f"\n规则 ID 列表:")
        for r in self.state.get('rules', [])[:5]:
            print(f"  {r['id']}: {r['content']}")
        print("  ...")
        print(f"\n完成反馈后执行:")
        print(f"  python scripts/rlhf_manager.py complete-episode")

        return episode

    def batch_feedback(self, feedback_file: str):
        """从文件批量导入反馈

        文件格式（每行一条）:
        rule_id,signal,comment
        rule_001,1.0,金句很好
        rule_005,-0.5,开头太平
        """
        path = Path(feedback_file)
        if not path.exists():
            print(f"文件不存在: {feedback_file}")
            return

        episode = self.state.get('current_episode')
        if not episode:
            print("没有进行中的 episode，请先 import-episode 或 start-episode")
            return

        content = path.read_text(encoding='utf-8')
        count = 0

        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(',')
            if len(parts) < 2:
                continue

            rule_id = parts[0].strip()
            try:
                signal = float(parts[1].strip())
            except:
                continue

            comment = parts[2].strip() if len(parts) > 2 else ''

            self.record_feedback(rule_id, signal, comment)
            count += 1

        print(f"\n已导入 {count} 条反馈")


def main():
    parser = argparse.ArgumentParser(description='RLHF Loop 自进化系统管理器')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化规则库')
    init_parser.add_argument('--force', action='store_true', help='强制重新初始化')

    # start-episode 命令
    start_parser = subparsers.add_parser('start-episode', help='开始新 episode')
    start_parser.add_argument('--mode', default='原创', choices=['原创', '素材重构'], help='创作模式')
    start_parser.add_argument('--topic', default='', help='主题')

    # apply-rules 命令
    subparsers.add_parser('apply-rules', help='获取本次应用的规则')

    # record-feedback 命令
    feedback_parser = subparsers.add_parser('record-feedback', help='记录反馈')
    feedback_parser.add_argument('rule_id', help='规则 ID')
    feedback_parser.add_argument('signal', type=float, choices=[1.0, 0.5, 0.0, -0.5, -1.0], help='反馈信号')
    feedback_parser.add_argument('--comment', default='', help='评论')

    # record-revision 命令
    subparsers.add_parser('record-revision', help='记录一次修改')

    # complete-episode 命令
    complete_parser = subparsers.add_parser('complete-episode', help='完成当前 episode')
    complete_parser.add_argument('--adopted', action='store_true', default=True, help='是否采用')
    complete_parser.add_argument('--rejected', action='store_true', help='不采用')

    # update-scores 命令
    subparsers.add_parser('update-scores', help='更新规则得分')

    # consolidate 命令
    subparsers.add_parser('consolidate', help='整合规则')

    # report 命令
    subparsers.add_parser('report', help='输出进化报告')

    # export 命令
    export_parser = subparsers.add_parser('export', help='导出规则')
    export_parser.add_argument('--output', help='输出文件路径')

    # reset 命令
    reset_parser = subparsers.add_parser('reset', help='重置进化状态')
    reset_parser.add_argument('--confirm', action='store_true', help='确认重置')

    # add-rule 命令
    add_parser = subparsers.add_parser('add-rule', help='添加新规则')
    add_parser.add_argument('category', help='规则分类')
    add_parser.add_argument('content', help='规则内容')
    add_parser.add_argument('--priority', default='medium', choices=['high', 'medium', 'low'], help='优先级')

    # remove-rule 命令
    remove_parser = subparsers.add_parser('remove-rule', help='删除规则')
    remove_parser.add_argument('rule_id', help='规则 ID')

    # list-articles 命令
    subparsers.add_parser('list-articles', help='列出所有历史文章')

    # import-episode 命令
    import_parser = subparsers.add_parser('import-episode', help='导入历史文章')
    import_parser.add_argument('article_path', help='文章路径')
    import_parser.add_argument('--mode', default='原创', choices=['原创', '素材重构'], help='创作模式')
    import_parser.add_argument('--revisions', type=int, default=0, help='修改次数')
    import_parser.add_argument('--rejected', action='store_true', help='标记为未采用')

    # batch-feedback 命令
    batch_parser = subparsers.add_parser('batch-feedback', help='从文件批量导入反馈')
    batch_parser.add_argument('feedback_file', help='反馈文件路径（CSV 格式）')

    # 状态文件参数
    parser.add_argument('--state-file', help='指定状态文件路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = RLHFManager(state_file=args.state_file)

    if args.command == 'init':
        manager.init(force=args.force)
    elif args.command == 'start-episode':
        manager.start_episode(mode=args.mode, topic=args.topic)
    elif args.command == 'apply-rules':
        manager.apply_rules()
    elif args.command == 'record-feedback':
        manager.record_feedback(args.rule_id, args.signal, args.comment)
    elif args.command == 'record-revision':
        manager.record_revision()
    elif args.command == 'complete-episode':
        manager.complete_episode(adopted=not args.rejected)
    elif args.command == 'update-scores':
        manager.update_scores()
    elif args.command == 'consolidate':
        manager.consolidate()
    elif args.command == 'report':
        manager.report()
    elif args.command == 'export':
        manager.export_rules(output_file=args.output)
    elif args.command == 'reset':
        manager.reset(confirm=args.confirm)
    elif args.command == 'add-rule':
        manager.add_rule(args.category, args.content, args.priority)
    elif args.command == 'remove-rule':
        manager.remove_rule(args.rule_id)
    elif args.command == 'list-articles':
        manager.list_articles()
    elif args.command == 'import-episode':
        manager.import_episode(
            args.article_path,
            mode=args.mode,
            adopted=not args.rejected,
            revisions=args.revisions
        )
    elif args.command == 'batch-feedback':
        manager.batch_feedback(args.feedback_file)


if __name__ == '__main__':
    main()
