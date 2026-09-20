# 求职小助手 Agent（JobMatch Agent）

一个面向求职场景的个人 AI Agent：输入**岗位 JD** 与**你的简历**，输出
**匹配度分析、简历优化建议、面试题准备**。

> 这是我的个人作品，用于实践 AI Agent 的核心能力（提示词设计、工具调用、
> 记忆管理、RAG），并把源文件开源以证明是本人从 0 到 1 完成。

## 设计思路

| Agent 能力 | 本项目落地 |
|---|---|
| 系统提示词（Persona） | `persona.md` 定义「资深求职顾问」人设、约束与输出格式 |
| 工具调用（Tool Use） | `jobmatch.py` 读取 JD / 简历文件、做关键词与技能提取 |
| 记忆（Memory） | 保存用户简历画像 `profile.json`，跨轮复用，避免重复输入 |
| RAG（检索增强） | 预留：可将历史岗位库 / 简历库做向量检索（见 roadmap） |
| 自写代码（L5） | `jobmatch.py` 纯标准库实现，规则基线无需任何 API Key |

## 架构（数据流）

```
   JD 文本 ─┐
            ├─► jobmatch.py ─► [提取关键词/技能] ─► [匹配计算] ─► 报告
   简历文本 ─┘                                          │
                                                      ├─ 匹配度评分
                                                      ├─ 简历优化建议
                                                      └─ 面试题准备
                              （可选）LLM 增强：设置 OPENAI_API_KEY 后调用
```

## 目录结构

```
job-agent/
├── README.md            # 本说明
├── persona.md           # 专家人设（L1）
├── jobmatch.py          # 核心脚本：规则基线 + 可选 LLM（L5）
└── skills/
    └── job-match/
        └── SKILL.md     # WorkBuddy 技能定义（L2，可直接加载）
```

## 快速开始

```bash
# 规则基线（无需 API Key，开箱即跑）
python jobmatch.py --jd jd.txt --resume resume.txt

# 可选：接入 LLM 做更自然的建议
set OPENAI_API_KEY=sk-xxx
python jobmatch.py --jd jd.txt --resume resume.txt --llm
```

## WorkBuddy 内使用

把 `skills/job-match/` 放到 `~/.workbuddy/skills/` 后，在 WorkBuddy 中即可
直接调用「求职匹配」技能：贴入 JD 与简历，得到分析报告。

## Roadmap（对应我的学习路线）

- [x] L1 专家（Persona）
- [x] L2 技能（SKILL.md，可在 WorkBuddy 加载）
- [x] L5 自写代码（jobmatch.py）
- [ ] L3 MCP：接入文件系统 / 招聘网站搜索工具
- [ ] L4 自动化：每日定时抓取目标岗位并生成匹配简报
- [ ] RAG：简历库 / 岗位库向量检索
