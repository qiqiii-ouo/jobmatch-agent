# -*- coding: utf-8 -*-
"""用真实简历内容重画作品集里的简历预览图 resume-preview.png。"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "C:/Windows/Fonts/msyh.ttc"
W = 520
pad = 28
navy = (31, 58, 95)
navy2 = (44, 82, 130)
blue = (59, 130, 246)
ink = (31, 41, 55)
gray = (107, 114, 128)
line = (229, 231, 235)
white = (255, 255, 255)

font = ImageFont.truetype(FONT, 13)
font_sm = ImageFont.truetype(FONT, 11.5)
font_big = ImageFont.truetype(FONT, 25)
font_sec = ImageFont.truetype(FONT, 15)


def cw(ch):
    return 13 if ord(ch) > 127 else 7


def wrap(text, max_w, fnt):
    lines, cur, w = [], "", 0
    for ch in text:
        cur += ch
        w += cw(ch)
        if w > max_w:
            lines.append(cur)
            cur, w = "", 0
    if cur:
        lines.append(cur)
    return lines or [""]


def build():
    # 内容（来自真实简历 C:/Users/Administrator/Desktop/简历/改/简历-AI Agent方向.docx）
    sections = [
        ("教育经历", [
            "2023.09-2027.07  浙江越秀外国语学院  大数据管理与应用（本科）",
            "GPA 3.16/4，专业前 15%，获校三等奖学金",
            "主修：Python、数据结构、统计学、数据库、数据挖掘、大数据可视化、Linux",
        ]),
        ("实习经历", [
            "杭州雷鸣信息发展有限公司 · 商务/AI 内容实习生 · 2026.07-2026.09",
            "• Seedance 批量制作 AI 短剧，脚本→生成→剪辑→多平台发布，累计 50+ 条",
            "• ffmpeg 批处理脚本批量转码，单条耗时 5 分钟降至 5 秒左右",
            "• 基于自动化/Agent 平台搭建内容生产与上传流程，减少重复劳动",
            "• Excel 透视表统计播放/涨粉/互动并可视化，输出周报优化策略",
            "• 商务支持：合同归档、SOP 文档、NAS 素材库、ToDesk 协作",
            "河南格瑞斯体育 · 经理助理 · 2025.07-2025.09",
            "• 客户数据管控，对接新客户，转化率 70%、留客率 90%",
            "启智教育 · 社群运营 · 2024.09-2026.09",
            "• 社群活跃度提升至约 50%，促成多次续费与转介绍",
        ]),
        ("个人 AI Agent 项目", [
            "2026.06-至今 · 基于 WorkBuddy 从 0 到 1 搭建个人 Agent",
            "• 定制专家 / 开发 Skill / 配置 MCP 工具 / 定时自动化任务",
            "• 开源 GitHub: qiqiii-ouo/jobmatch-agent（含完整 commit 历史）",
            "• 掌握提示词设计、工具调用、记忆管理与 RAG 检索增强",
        ]),
        ("技能特长", [
            "• AI 工具：Seedance、剪映、ffmpeg 批处理、自动化/Agent 平台",
            "• Agent 构建：提示词工程、工具调用、记忆与 RAG",
            "• 数据：Excel 透视表与可视化、SPSS、数据挖掘分析",
            "• 综合：计算机二级、英语四级、社团社长（团队管理）",
        ]),
        ("自我评价", [
            "对 AI 应用落地有真实动手经验，学习能力强，能把新工具转为生产力；",
            "做事细致，有 SOP 沉淀与流程化意识，愿在 AI 产品一线快速成长。",
        ]),
    ]

    # 预估高度
    max_w = W - pad * 2 - 8
    h = 96  # 顶部
    for title, lines in sections:
        h += 30
        for ln in lines:
            for _ in wrap(ln, max_w, font):
                h += 20
    h += 40

    img = Image.new("RGB", (W, h), white)
    d = ImageDraw.Draw(img)
    # 顶部深蓝
    d.rectangle([0, 0, W, 92], fill=navy)
    d.text((pad, 16), "李舒晴", fill=white, font=font_big)
    d.text((pad, 52), "求职意向：AI 应用 / AI Agent 方向", fill=(219, 234, 254), font=font_sm)
    d.text((pad, 70), "21岁 · 女 · 2027届 | 14737117139 | 1609634529@qq.com", fill=(203, 213, 225), font=font_sm)

    y = 110
    for title, lines in sections:
        d.rectangle([pad, y, pad + 5, y + 16], fill=blue)
        d.text((pad + 12, y - 2), title, fill=navy, font=font_sec)
        y += 26
        d.line([pad, y, W - pad, y], fill=line, width=1)
        y += 12
        for ln in lines:
            if ln.startswith("•") or ln.startswith("20") or "·" in ln[:2]:
                wrapped = wrap(ln, max_w, font)
                for i, wl in enumerate(wrapped):
                    if i == 0 and ln.startswith("•"):
                        d.text((pad + 6, y), "•", fill=blue, font=font)
                        d.text((pad + 18, y), wl[1:].strip(), fill=ink, font=font)
                    else:
                        d.text((pad + 6, y), wl, fill=ink, font=font)
                    y += 20
            else:
                for wl in wrap(ln, max_w, font):
                    d.text((pad + 6, y), wl, fill=ink, font=font)
                    y += 20
        y += 14

    d.text((pad, h - 26), "← 作品集内简历预览（完整版见真实 .docx）", fill=gray, font=font_sm)

    out = os.path.join(BASE, "resume-preview.png")
    img.save(out)
    print("resume-preview.png 已用真实简历重画:", os.path.getsize(out) // 1024, "KB,", h, "px 高")


if __name__ == "__main__":
    build()
