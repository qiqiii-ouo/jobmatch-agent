#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
求职小助手 Agent —— 核心脚本（L5 自写代码）

功能：输入岗位 JD 与简历文本，输出匹配度分析、简历优化建议、面试题预测。
- 规则基线：纯标准库实现，无需任何 API Key，开箱即跑。
- 可选 LLM：设置 OPENAI_API_KEY 后加 --llm，调用 OpenAI 兼容接口生成更自然建议。

用法：
    python jobmatch.py --jd jd.txt --resume resume.txt
    python jobmatch.py --jd jd.txt --resume resume.txt --llm
"""
import argparse
import json
import os
import re
import sys
import urllib.request

# 常见岗位能力关键词词典（用于提取与匹配）
SKILL_LEXICON = [
    "python", "sql", "excel", "数据透视表", "可视化", "数据分析", "数据挖掘",
    "机器学习", "深度学习", "大模型", "llm", "agent", "prompt", "提示词",
    "自动化", "ffmpeg", "剪映", "seedance", "spss", "linux", "github",
    "需求分析", "用户调研", "项目管理", "社群运营", "内容运营", "产品运营",
    "统计", "数据库", "r", "tableau", "power bi", "n8n", "mcp",
]

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_keywords(text):
    """从文本中提取能力关键词（小写匹配）。"""
    low = text.lower()
    found = [kw for kw in SKILL_LEXICON if kw in low]
    return found

def jaccard(a, b):
    if not a and not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)

def rule_analysis(jd_text, resume_text):
    jd_kw = extract_keywords(jd_text)
    rs_kw = extract_keywords(resume_text)
    score = round(jaccard(jd_kw, rs_kw) * 100)
    matched = sorted(set(jd_kw) & set(rs_kw), key=jd_kw.index)
    missing = [kw for kw in jd_kw if kw not in rs_kw]
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "jd_keywords": jd_kw,
        "resume_keywords": rs_kw,
    }

def llm_enhance(jd_text, resume_text, analysis):
    """可选：调用 OpenAI 兼容接口生成建议。"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    prompt = (
        "你是资深求职顾问。以下是岗位JD和简历，请给匹配度、优化建议、面试题。\n"
        f"【JD】\n{jd_text}\n\n【简历】\n{resume_text}\n\n"
        f"已提取的关键词匹配：{json.dumps(analysis, ensure_ascii=False)}"
    )
    body = json.dumps({
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }).encode("utf-8")
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
    except Exception as e:  # 失败则回退规则
        print(f"[warn] LLM 调用失败，回退规则版：{e}", file=sys.stderr)
        return None

def render(analysis, llm_text=None):
    lines = []
    lines.append("【匹配度】%d / 100" % analysis["score"])
    lines.append("")
    lines.append("【优势】")
    for kw in analysis["matched"]:
        lines.append(f"  + 命中岗位关键词：{kw}")
    if not analysis["matched"]:
        lines.append("  （暂无明显命中，建议补充相关项目/技能）")
    lines.append("")
    lines.append("【待补强】（JD 要求但简历缺失，建议补充真实经历或相关学习）")
    for kw in analysis["missing"][:8]:
        lines.append(f"  - {kw}：用真实项目/课程补充，不要虚构")
    if not analysis["missing"]:
        lines.append("  （关键词覆盖较好）")
    lines.append("")
    lines.append("【面试题预测】")
    sample = analysis["missing"][:3] if analysis["missing"] else analysis["matched"][:3]
    for i, kw in enumerate(sample, 1):
        lines.append(f"  {i}. 请讲一个你运用「{kw}」解决实际问题的例子。")
    if llm_text:
        lines.append("")
        lines.append("【LLM 增强建议】")
        lines.append(llm_text)
    return "\n".join(lines)

def save_profile(resume_text, path="profile.json"):
    """记忆：缓存简历画像（关键词），跨轮复用。"""
    kw = extract_keywords(resume_text)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"resume_keywords": kw}, f, ensure_ascii=False, indent=2)

def main():
    ap = argparse.ArgumentParser(description="求职小助手 Agent：JD-简历匹配分析")
    ap.add_argument("--jd", required=True, help="岗位 JD 文本文件路径")
    ap.add_argument("--resume", required=True, help="简历文本文件路径")
    ap.add_argument("--llm", action="store_true", help="启用 LLM 增强（需 OPENAI_API_KEY）")
    args = ap.parse_args()

    jd_text = read_text(args.jd)
    resume_text = read_text(args.resume)
    analysis = rule_analysis(jd_text, resume_text)
    llm_text = llm_enhance(jd_text, resume_text, analysis) if args.llm else None

    print(render(analysis, llm_text))
    save_profile(resume_text)
    print("\n[info] 简历画像已缓存到 profile.json（记忆示例）", file=sys.stderr)

if __name__ == "__main__":
    main()
