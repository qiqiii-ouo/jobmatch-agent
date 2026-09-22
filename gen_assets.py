# -*- coding: utf-8 -*-
"""生成作品集素材：项目演示 GIF（终端打字动画）+ 简历预览 PNG。"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑，支持中英文

# ---------- 1) 项目演示 GIF：终端打字动画 ----------
def make_demo_gif():
    W, H = 760, 600
    bg = (15, 23, 42)
    fg = (226, 232, 240)
    green = (134, 239, 172)
    cyan = (125, 211, 252)
    amber = (253, 230, 138)
    gray = (148, 163, 184)
    font = ImageFont.truetype(FONT, 15)
    lh = 23
    pad = 22

    # 命令 + 真实运行输出
    cmd = "$ python jobmatch.py --jd jd.txt --resume resume.txt"
    with open(os.path.join(BASE, "demo_output.txt"), encoding="utf-8") as f:
        out = f.read().rstrip("\n")
    lines = [cmd] + out.split("\n")
    # 给输出行上色：命令青色，[info]灰，匹配度/标题亮色
    def color_of(line):
        if line.startswith("$"):
            return cyan
        if line.startswith("[info]"):
            return gray
        if "匹配度" in line:
            return amber
        if line.startswith("【"):
            return green
        if line.startswith(("+", "-")):
            return fg
        if line[0:1].isdigit() and "." in line[:3]:
            return fg
        return fg

    frames = []

    def render(shown_full, partial):
        img = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(img)
        # 顶部装饰条
        d.rectangle([0, 0, W, 34], fill=(30, 41, 59))
        for i, c in enumerate([(248, 113, 113), (251, 191, 36), (134, 239, 172)]):
            d.ellipse([16 + i * 20, 12, 26 + i * 20, 22], fill=c)
        d.text((90, 9), "jobmatch — terminal", fill=(148, 163, 184), font=font)
        y = 44
        for ln in shown_full:
            d.text((pad, y), ln, fill=color_of(ln), font=font)
            y += lh
        if partial:
            d.text((pad, y), partial, fill=color_of(partial), font=font)
        return img

    shown = []
    for line in lines:
        # 逐字打字，每帧加 2 字符，控制帧数
        if not line:
            shown.append("")
            continue
        for i in range(2, len(line) + 1, 2):
            frames.append(render(shown, line[:i]))
        frames.append(render(shown, line))  # 整行定格
        shown.append(line)
    # 末尾停留
    for _ in range(12):
        frames.append(render(shown, ""))

    gif_path = os.path.join(BASE, "demo.gif")
    frames[0].save(
        gif_path, save_all=True, append_images=frames[1:],
        duration=45, loop=0, optimize=True,
    )
    print("demo.gif 生成:", len(frames), "帧,", os.path.getsize(gif_path) // 1024, "KB")


# ---------- 2) 简历预览 PNG ----------
def make_resume_preview():
    W, H = 500, 720
    white = (255, 255, 255)
    navy = (31, 58, 95)
    navy2 = (44, 82, 130)
    blue = (59, 130, 246)
    ink = (31, 41, 55)
    gray = (107, 114, 128)
    line = (229, 231, 235)
    font = ImageFont.truetype(FONT, 15)
    font_sm = ImageFont.truetype(FONT, 12)
    font_big = ImageFont.truetype(FONT, 26)

    img = Image.new("RGB", (W, H), white)
    d = ImageDraw.Draw(img)

    # 顶部深蓝区
    d.rectangle([0, 0, W, 96], fill=navy)
    d.text((28, 20), "李舒晴", fill=white, font=font_big)
    d.text((28, 58), "求职意向：AI Agent 方向", fill=(219, 234, 254), font=font)
    d.text((28, 78), "大数据管理与应用 · 2027 届 · GPA 3.11/4", fill=(203, 213, 225), font=font_sm)

    y = 120

    def section(title):
        nonlocal y
        d.rectangle([28, y, 34, y + 16], fill=blue)
        d.text((44, y - 2), title, fill=navy, font=font)
        y += 26
        d.line([28, y, W - 28, y], fill=line, width=1)
        y += 14

    def kv(k, v):
        nonlocal y
        d.text((28, y), k, fill=gray, font=font_sm)
        d.text((120, y), v, fill=ink, font=font_sm)
        y += 22

    def bullet(text):
        nonlocal y
        d.text((34, y), "•", fill=blue, font=font_sm)
        d.text((50, y), text, fill=ink, font=font_sm)
        y += 20

    section("教育背景")
    kv("学校", "浙江越秀外国语学院")
    kv("专业", "大数据管理与应用（2027 届）")
    kv("成绩", "GPA 3.11/4 · 专业前 15%")
    y += 6

    section("实习经历")
    kv("公司", "杭州雷鸣信息发展有限公司")
    kv("岗位", "商务 / AI 内容运营实习生")
    kv("时间", "2026.07 – 2026.09")
    y += 2
    bullet("AI 短剧全流程：脚本→Seedance→剪辑→多平台发布")
    bullet("ffmpeg 批量处理脚本，提升视频处理效率")
    bullet("搭建内容生产自动化流程，减少重复操作")
    bullet("账号数据分析与可视化，输出周报优化策略")
    y += 6

    section("项目经历")
    kv("作品", "求职小助手 Agent（开源）")
    bullet("GitHub: qiqiii-ouo/jobmatch-agent")
    bullet("输入 JD+简历→匹配度/优化/面试题")
    y += 6

    section("技能")
    kv("AI/数据", "Python · Excel · 透视表 · ffmpeg")
    kv("工具", "Seedance · 剪映 · WorkBuddy · 自动化")

    # 底部水印
    d.text((28, H - 24), "← 作品集内简历预览（完整版见 .docx）", fill=gray, font=font_sm)

    png_path = os.path.join(BASE, "resume-preview.png")
    img.save(png_path)
    print("resume-preview.png 生成:", os.path.getsize(png_path) // 1024, "KB")


if __name__ == "__main__":
    make_demo_gif()
    make_resume_preview()
