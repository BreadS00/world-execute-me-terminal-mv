#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
world.execute(me) -- a terminal ascii music video (single file, zero deps)

The terminal you are looking at is not a player.  It is "me".
Running this script IS the act of world.execute(me):
boot, love, loss, execution, termination -- all of it is my output.

usage:
  python world_execute_me_mv.py                          play the whole song
  python world_execute_me_mv.py --audio song.mp3 --offset -0.5
                                                         open song in default
                                                         player, fine-tune sync
  python world_execute_me_mv.py --shots                  export keyframes to shots/
  python world_execute_me_mv.py --shot 120,205           print frame(s) at time(s)
  python world_execute_me_mv.py --fps 24                 frame rate

keys during playback: q / Esc -> terminate me.  Ctrl+C works too.
"""

import argparse
import math
import os
import random
import re
import shutil
import sys
import time
import unicodedata

# ---------------------------------------------------------------- constants
PROG = "world.execute(me)"
FPS_DEFAULT = 30
MIN_W, MIN_H = 80, 25
LRC_FILENAME = "world.execute (me)_LRC歌词_中英.txt"

# built-in copy of the LRC (used when the external file is missing)
LRC_TEXT = r"""
[0000.27]Switch on the power line
[0001.93]接上电源
[0001.93]Remember to put on protection
[0003.95]记得装备好绝缘护具
[0003.95]Lay down your pieces
[0005.57]摆好棋子
[0005.57]And let's begin object creation
[0007.60]开始吧对象生成
[0007.60]Fill in my data parameters initialisation
[0011.24]输入我的参数 并初始化
[0011.24]Setup our new world
[0012.93]选择一个我们的世界
[0012.93]And let's begin the simulation
[0029.74]然后让我们开始一场模拟游戏
[0029.74]If I'm a set of points
[0031.37]如果我是一组点
[0031.37]Then I will give you my dimension
[0033.42]那么我将献给你我的另个次元
[0033.42]If I'm a circle
[0034.98]如果我是一个圆
[0034.98]Then I will give you my circumference
[0037.15]那么我将献给你我的圆周
[0037.15]If I'm a sine wave
[0038.73]如果我是一条正弦波
[0038.73]Then you can sit on all my tangents
[0040.78]那你可以给予我一套切线
[0040.78]If I approach infinity
[0042.42]如果我趋近于无限 那你这是我的
[0042.42]Then you can be my limitations
[0044.48]我的一个极限
[0044.48]Switch my current
[0046.13]切换我的电流
[0046.13]To AC to DC
[0047.94]从交流到直流
[0047.94]And then blind my vision
[0049.78]然后蒙上我的眼睛
[0049.78]So dizzy so dizzy
[0051.38]让我头晕目眩
[0051.38]Oh we can travel
[0053.48]我们可以穿越时空
[0053.48]To A.D to B.C
[0055.17]从公元前到现代
[0055.17]And we can unite
[0057.17]然后合成一体
[0057.17]So deeply so deeply
[0059.40]深深陷入这潭沼泽
[0059.40]If I can
[0100.20]如果我能
[0100.20]If I can give you all the stimulations
[0102.92]如果我能够给你终极刺激
[0102.92]Then I can
[0103.86]那么我就能够
[0103.86]Then I can be your only satisfaction
[0106.62]那么我就能够成为你唯一的慰藉
[0106.62]If I can make you happy
[0108.48]如果我能够让你开心
[0108.48]I will run the execution
[0110.32]那么我将执行指令
[0110.32]Though we are trapped
[0111.76]但我们被困
[0111.76]In this strange strange simulation
[0114.04]在这个异乎寻常的模拟程序之中
[0114.04]If I'm an eggplant
[0115.68]如果我是一根茄子
[0115.68]Then I will give you my nutrients
[0117.70]那么我将献给你我所有营养
[0117.70]If I'm a tomato
[0119.32]如果我是一颗番茄
[0119.32]Then I'll give you antioxidants
[0121.37]那么我将献给你我的抗氧化物
[0121.37]If I'm a tabby cat
[0123.06]如果我是一只花猫
[0123.06]Then I will purr for your enjoyment
[0125.13]那么我将为你咕噜咕噜 只要你喜欢
[0125.13]If I'm the only god
[0126.74]如果我是唯一的神
[0126.74]Then you're the proof of my existence
[0128.78]那么你将是我存在的证明
[0128.78]Switch my gender
[0130.34]切换我的性别
[0130.34]To F to M
[0132.13]从女到男
[0132.13]And then do whatever
[0134.09]只做想做的事
[0134.09]From AM to PM
[0135.78]从早到晚
[0135.78]Oh switch my role
[0137.72]切换我的角色
[0137.72]To S to M
[0139.58]从施虐者到被虐者
[0139.58]So we can enter
[0141.35]这样我们就可以
[0141.35]The trance the trance
[0143.48]享受你我 恍惚出神
[0143.48]If I can
[0144.48]如果我能
[0144.48]If I can feel your vibrations
[0147.22]如果我能够感受到你的振动
[0147.22]Then I can
[0148.16]那么我就能够
[0148.16]Then I can finally be completion
[0150.92]那么我就终于能够完成任务
[0150.92]Though you have left
[0152.33]但你却是离开了
[0152.33]You have left
[0153.25]你还是离开了
[0153.25]You have left
[0154.18]你对我说了再见
[0154.18]You have left
[0155.08]你还是离开了
[0155.08]You have left
[0156.03]你对我说了再见
[0156.03]You have left me in isolation
[0158.34]你独留我于独孤之中
[0158.34]If I can
[0159.22]如果我能
[0159.22]If I can erase all the pointless fragments
[0202.02]如果我能够删除那些无用碎片
[0202.02]Then maybe
[0202.97]那么或许我
[0202.97]Then maybe you won't leave me so disheartened
[0205.67]那么或许我就不会如此失望
[0205.67]Challenging your god
[0209.04]与神做对
[0209.04]You have made some illegal arguments
[0227.86]你给我的是非法参数
[0227.86]Execution execution execution execution
[0231.56]执行 执行 死刑
[0231.56]Execution execution execution execution
[0235.22]执行 执行 死刑
[0235.22]Execution execution execution execution
[0238.95]执行 执行 死刑
[0238.95]Ein Dos Trois Ne Fem Liu
[0241.72]一 二 三 四 五 六
[0241.72]Execution
[0242.72]死刑
[0242.72]If I can
[0243.60]如果我能
[0243.60]If I can give them all the execution
[0246.31]如果我能够给所有人执行死刑
[0246.31]Then I can
[0247.24]那我就是
[0247.24]Then I can be your only execution
[0249.99]那我就是你唯一指令
[0249.99]If I can have you back
[0251.95]如果你能够回到我身边
[0251.95]I will run the execution
[0253.70]那么我将执行死刑
[0253.70]Though we are trapped
[0255.14]尽管我们围困其中
[0255.14]We are trapped ah
[0257.41]我们围困其中
[0257.41]I've studied
[0258.30]我学会了
[0258.30]I've studied how to properly lo-o-ove
[0301.16]我学会了如何好好去爱
[0301.16]Question me
[0302.09]提问我吧
[0302.09]Question me I can answer all lo-o-ove
[0304.83]提问我吧 只要是爱的问题 我全都能答对
[0304.83]I know the algebraic expression of lo-o-ove
[0308.48]就连爱的代数表达式我都知道
[0308.48]Though you are free
[0309.89]虽然你已自由
[0309.89]I am trapped
[0310.77]我仍被困
[0310.77]Trapped in lo-o-ove
[0325.96]困于爱里
[0325.96]Execution
[0330.096]执行死刑
[0330.096]"""

# the six "You have left" hits and the 12-execution block (song seconds)
T_LEFT6 = [112.33, 113.25, 114.18, 115.08, 116.03, 118.34]
T_EXEC12 = 151.56
T_COUNT6 = 161.72          # Ein Dos Trois Ne Fem Liu
RITUAL_START = 209.5
TOTAL_END = 230.0

# ---------------------------------------------------------------- palette
C = {
    "green":  "55ff99", "dgreen": "2fae6e", "lime": "7dff6e",
    "pink":   "ff7ab8", "dpink":  "b5528a", "hotpink": "ff4fa0",
    "cyan":   "4de8ff", "dcyan":  "2a93a8",
    "yellow": "ffd24d", "dyellow":"9c7d1e",
    "blue":   "6f9fff", "dblue":  "39559c", "night":  "3f5f9f",
    "red":    "ff4444", "dred":   "8a1f1f", "hot":    "ff2a2a",
    "magenta":"ff44ff", "dmag":   "8a1f8a",
    "white":  "f2f2f2", "gray":   "8a8a8a", "dgray":  "4a4a4a",
    "vdgray": "262626", "violet": "b98cff", "gold":   "ffd700",
    "orange": "ffa552", "chalk":  "cfe8ff", "rest":   "8899aa",
    "black":  "101010",
}

def rgb(h):
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def hx(r, g, b):
    return "%02x%02x%02x" % (max(0, min(255, int(r))), max(0, min(255, int(g))),
                             max(0, min(255, int(b))))

def desat(h, s):
    """s=1 -> original color, s=0 -> pure gray."""
    if not h or s >= 1.0:
        return h
    r, g, b = rgb(h)
    m = (r * 299 + g * 587 + b * 114) // 1000
    return hx(m + (r - m) * s, m + (g - m) * s, m + (b - m) * s)

def dimc(h, f):
    """f=1 -> original, f=0 -> black."""
    if not h or f >= 1.0:
        return h
    r, g, b = rgb(h)
    return hx(r * f, g * f, b * f)

def mix(a, b, f):
    if not a:
        return b
    if not b:
        return a
    r1, g1, b1 = rgb(a)
    r2, g2, b2 = rgb(b)
    return hx(r1 + (r2 - r1) * f, g1 + (g2 - g1) * f, b1 + (b2 - b1) * f)

def hsv(hdeg, s, v):
    hdeg = (hdeg % 360.0) / 60.0
    i = int(hdeg)
    f = hdeg - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    return ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))[i % 6]

def hue_hex(hdeg, s=0.75, v=1.0):
    r, g, b = hsv(hdeg, s, v)
    return hx(r * 255, g * 255, b * 255)

def frame_rnd(t):
    return random.Random(int(t * 1000) & 0xFFFFFFFF)

def hsh(*a):
    """fast deterministic 0..1 hash"""
    h = 2166136261
    for v in a:
        h = ((h ^ int(v)) * 16777619) & 0xFFFFFFFF
    return (h % 1000003) / 1000003.0

def clamp(v, a, b):
    return a if v < a else (b if v > b else v)

def lerp(a, b, f):
    return a + (b - a) * f

# ---------------------------------------------------------------- lyrics
_LRC_LINE = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)\](.*)$")        # [mm:ss.xx]
_LRC_LINE2 = re.compile(r"^\[(\d{2})(\d{2}(?:\.\d+)?)\](.*)$")   # [mmss.xx]

def _is_zh(s):
    return any("\u4e00" <= ch <= "\u9fff" for ch in s)

def parse_lrc(text):
    """returns list of dicts {t, en, zh}; zh lines attach to previous en line."""
    out = []
    for raw in text.splitlines():
        s = raw.strip()
        m = _LRC_LINE.match(s) or _LRC_LINE2.match(s)
        if not m:
            continue
        t = int(m.group(1)) * 60.0 + float(m.group(2))
        body = m.group(3).strip()
        if not body:
            continue
        if _is_zh(body):
            if out:
                out[-1]["zh"] = body
        else:
            out.append({"t": t, "en": body, "zh": ""})
    return out

def load_lyrics():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(os.getcwd(), LRC_FILENAME),
                 os.path.join(here, LRC_FILENAME)):
        try:
            with open(cand, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
            if "[" in txt and "]" in txt:
                ly = parse_lrc(txt)
                if ly:
                    return ly, cand
        except OSError:
            pass
    return parse_lrc(LRC_TEXT), "<built-in copy>"

LYRICS, LRC_SOURCE = load_lyrics()
T_END = LYRICS[-1]["t"] if LYRICS else 205.96   # 100% mark: the last sung line

# keyword colouring inside the current lyric line
_KW = [
    ("execution", "red"), ("lo-o-ove", "pink"), ("love", "pink"),
    ("trapped", "cyan"), ("isolation", "cyan"), ("infinity", "cyan"),
    ("trance", "cyan"), ("simulation", "cyan"),
    ("your", "cyan"), ("you", "cyan"), ("left", "cyan"),
    ("god", "cyan"), ("free", "cyan"),
]
_KW_PAT = re.compile("|".join(r"\b" + re.escape(w) + r"\b" for w, _ in
                              sorted(_KW, key=lambda p: -len(p[0]))), re.I)
_KW_MAP = dict(_KW)

def lyric_segments(en):
    """split en into [(text, color-or-None, upper)] with keywords emphasised"""
    segs = []
    pos = 0
    for m in _KW_PAT.finditer(en):
        if m.start() > pos:
            segs.append((en[pos:m.start()], None, False))
        segs.append((m.group(0), _KW_MAP[m.group(0).lower()], True))
        pos = m.end()
    if pos < len(en):
        segs.append((en[pos:], None, False))
    return segs

def dw(s):
    """display width (CJK counts 2)"""
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return w

def dw_cut(s, width):
    """cut s to at most `width` display columns"""
    out = []
    w = 0
    for ch in s:
        cw = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if w + cw > width:
            break
        out.append(ch)
        w += cw
    return "".join(out)

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h):
        self.w = int(w)
        self.h = int(h)
        self.ch = [[" "] * self.w for _ in range(self.h)]
        self.fg = [[None] * self.w for _ in range(self.h)]
        self.bg = [[None] * self.w for _ in range(self.h)]
        self.fx = {"shake": 0.0, "flash": None, "sat": 1.0, "dim": 1.0}
        self.rnd = random.Random(1)

    def clear(self):
        for y in range(self.h):
            self.ch[y] = [" "] * self.w
            self.fg[y] = [None] * self.w
            self.bg[y] = [None] * self.w

    def put(self, x, y, s, fg=None, bg=None):
        y = int(y)
        x = int(x)
        if y < 0 or y >= self.h or x >= self.w or not s:
            return
        row_ch, row_fg, row_bg = self.ch[y], self.fg[y], self.bg[y]
        for i, ch in enumerate(s):
            xx = x + i
            if xx < 0:
                continue
            if xx >= self.w:
                break
            row_ch[xx] = ch
            row_fg[xx] = fg
            row_bg[xx] = bg

    def putc(self, x, y, ch, fg=None, bg=None):
        x = int(x)
        y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.ch[y][x] = ch
            self.fg[y][x] = fg
            self.bg[y][x] = bg

    def text_center(self, y, s, fg=None, bg=None):
        if s:
            self.put((self.w - dw(s)) // 2, y, s, fg, bg)

    def text_right(self, y, s, fg=None, bg=None):
        if s:
            self.put(self.w - dw(s) - 1, y, s, fg, bg)

    def text_left(self, y, s, fg=None, x=1, bg=None):
        self.put(x, y, s, fg, bg)

    def hline(self, x0, x1, y, ch="=", fg=None):
        self.put(x0, y, ch * max(0, x1 - x0 + 1), fg)

    def vline(self, x, y0, y1, ch="|", fg=None):
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            self.putc(x, y, ch, fg)

    def frame(self, x, y, w, h, fg=None, ch=("+", "-", "|")):
        self.put(x, y, ch[0] + ch[1] * (w - 2) + ch[2], fg)
        self.put(x, y + h - 1, ch[0] + ch[1] * (w - 2) + ch[2], fg)
        for yy in range(y + 1, y + h - 1):
            self.putc(x, yy, ch[2], fg)
            self.putc(x + w - 1, yy, ch[2], fg)

    def circle(self, cx, cy, r, fg=None, chars="*"):
        """aspect-corrected circle (y compressed ~0.5)"""
        if r < 1:
            self.putc(int(cx), int(cy), chars[0], fg)
            return
        steps = max(12, int(r * 7))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.putc(int(round(cx + r * math.cos(a))),
                      int(round(cy + r * 0.5 * math.sin(a))),
                      chars[i % len(chars)], fg)

    def glitch(self, density, colors):
        n = int(density * self.w * self.h)
        syms = "#@%&$?!*<>/:;"
        for _ in range(n):
            x = self.rnd.randrange(self.w)
            y = self.rnd.randrange(self.h)
            self.ch[y][x] = syms[self.rnd.randrange(len(syms))]
            self.fg[y][x] = colors[self.rnd.randrange(len(colors))]
            self.bg[y][x] = None

    def dropout(self, keep, salt):
        """keep only `keep` fraction of non-space chars (deterministic)"""
        for y in range(self.h):
            for x in range(self.w):
                if self.ch[y][x] != " " and hsh(x, y, salt) > keep:
                    self.ch[y][x] = " "

    def shifted(self, dx, dy):
        if dx == 0 and dy == 0:
            return
        ch = [[" "] * self.w for _ in range(self.h)]
        fg = [[None] * self.w for _ in range(self.h)]
        bg = [[None] * self.w for _ in range(self.h)]
        for y in range(self.h):
            sy = y - dy
            if 0 <= sy < self.h:
                row = self.ch[sy]
                if dx == 0:
                    ch[y] = row[:]
                    fg[y] = self.fg[sy][:]
                    bg[y] = self.bg[sy][:]
                else:
                    for x in range(self.w):
                        sx = x - dx
                        if 0 <= sx < self.w:
                            ch[y][x] = row[sx]
                            fg[y][x] = self.fg[sy][sx]
                            bg[y][x] = self.bg[sy][sx]
        self.ch, self.fg, self.bg = ch, fg, bg

# ---------------------------------------------------------------- 5x5 font
FONT5 = {
 "A": ["..#..",".#.#.","#...#","#####","#...#"],
 "B": ["####.","#...#","####.","#...#","####."],
 "C": [".####","#....","#....","#....",".####"],
 "D": ["####.","#...#","#...#","#...#","####."],
 "E": ["#####","#....","####.","#....","#####"],
 "F": ["#####","#....","####.","#....","#...."],
 "G": [".####","#....","#..##","#...#",".####"],
 "H": ["#...#","#...#","#####","#...#","#...#"],
 "I": ["#####","..#..","..#..","..#..","#####"],
 "J": ["..###","...#.","...#.","#..#.",".##.."],
 "K": ["#...#","#..#.","###..","#..#.","#...#"],
 "L": ["#....","#....","#....","#....","#####"],
 "M": ["#...#","##.##","#.#.#","#...#","#...#"],
 "N": ["#...#","##..#","#.#.#","#..##","#...#"],
 "O": [".###.","#...#","#...#","#...#",".###."],
 "P": ["####.","#...#","####.","#....","#...."],
 "Q": [".###.","#...#","#.#.#",".###.","....#"],
 "R": ["####.","#...#","####.","#..#.","#...#"],
 "S": [".####","#....",".###.","....#","####."],
 "T": ["#####","..#..","..#..","..#..","..#.."],
 "U": ["#...#","#...#","#...#","#...#",".###."],
 "V": ["#...#","#...#","#...#",".#.#.","..#.."],
 "W": ["#...#","#...#","#.#.#","##.##","#...#"],
 "X": ["#...#",".#.#.","..#..",".#.#.","#...#"],
 "Y": ["#...#",".#.#.","..#..","..#..","..#.."],
 "Z": ["#####","...#.","..#..",".#...","#####"],
 "0": [".###.","#..##","#.#.#","##..#",".###."],
 "1": ["..#..",".##..","..#..","..#..","#####"],
 "2": [".###.","#...#","..##.",".#...","#####"],
 "3": ["####.","....#",".###.","....#","####."],
 "4": ["#..#.","#..#.","#####","...#.","...#."],
 "5": ["#####","#....","####.","....#","####."],
 "6": [".###.","#....","####.","#...#",".###."],
 "7": ["#####","....#","...#.","..#..",".#..."],
 "8": [".###.","#...#",".###.","#...#",".###."],
 "9": [".###.","#...#",".####","....#",".###."],
 "!": ["..#..","..#..","..#..",".....","..#.."],
 "?": [".###.","#...#","..##.",".....","..#.."],
 ".": [".....",".....",".....",".....","..#.."],
 ",": [".....",".....",".....","..#..",".#..."],
 ":": [".....","..#..",".....","..#..","....."],
 "-": [".....",".....","#####",".....","....."],
 "_": [".....",".....",".....",".....","#####"],
 "+": [".....","..#..","#####","..#..","....."],
 "=": [".....","#####",".....","#####","....."],
 ">": ["...#.","..#..",".#...","..#..","...#."],
 "<": [".#...","..#..","...#.","..#..",".#..."],
 "'": ["..#..","..#..",".....",".....","....."],
 "/": ["....#","...#.","..#..",".#...","#...."],
 "(": ["...#.","..#..","..#..","..#..","...#."],
 ")": [".#...","..#..","..#..","..#..",".#..."],
 "%": ["#...#","...#.","..#..",".#...","#...#"],
 "*": ["#.#.#",".###.","#####",".###.","#.#.#"],
 "@": [".###.","#...#","#.###","#...#",".###."],
 "$": ["..#..",".####","..#..","####.","..#.."],
 "~": [".....",".##.#","..##.",".....","....."],
 " ": [".....",".....",".....",".....","....."],
}

def big_text(cv, cx, cy, s, fg, px=2, py=1, bg=None):
    s = s.upper()
    n = len(s)
    total_w = n * (5 * px + px) - px
    x0 = int(cx - total_w / 2)
    cy = int(cy)
    for i, chn in enumerate(s):
        g = FONT5.get(chn)
        if not g:
            continue
        gx = x0 + i * (5 * px + px)
        for gy in range(5):
            row = g[gy]
            run = ""
            for gxcol in range(5):
                run += (row[gxcol] * px)
            if "#" in run:
                cv.put(gx, cy + gy * py, run.replace(".", " "), fg, bg)

def big_width(s, px):
    return len(s) * 6 * px - px

def big_fit(s, maxw, maxh):
    """largest (px,py) so the text fits; chars are ~1:2 so py=px (tall blocks)"""
    px = max(1, (maxw + 1) // (6 * len(s)))
    py = max(1, min(px, maxh // 5))
    return px, py

# ---------------------------------------------------------------- art assets
ART = {}

ART["eggplant"] = (
    "        , /\n"
    "       / /\n"
    "      / /\n"
    "     / /\n"
    "  __/ /\n"
    " (____)\n"
    "(______)\n"
    "(______)\n"
    " (____)\n"
    "  `--'"
)

ART["tomato"] = (
    "     .-\"\"-.\n"
    "    /  _   \\\n"
    "   |  (_)  |\n"
    "   |   _   |\n"
    "    \\ (_) /\n"
    "     `-..-'\n"
    "       ^^"
)

ART["cat"] = (
    "      /\\_____/\\\n"
    "     /  o   o  \\\n"
    "    ( ==  ^  == )\n"
    "     )         (\n"
    "    (           )\n"
    "   ( (  )   (  ) )\n"
    "  (__(__)___(__)__)"
)

ART["tombstone"] = (
    "        .-~~~~~~-.\n"
    "       /          \\\n"
    "      |    R.I.P   |\n"
    "      |            |\n"
    "      |     me     |\n"
    "      |  process   |\n"
    "      |   no.2045  |\n"
    "      |  ran 03:26 |\n"
    "      | cause:love |\n"
    "   ___|____________|___\n"
    "  /____________________\\"
)

ART["figures"] = (
    "  o o\n"
    " /|\\ /|\\\n"
    " / \\ / \\\n"
    " me you"
)

ART["heartcage"] = (
    "   .-.-.-.-.-.\n"
    "  |  _   _   |\n"
    "  | ( \\./ )  |\n"
    "  |  \\ o /   |\n"
    "  |  /| |\\   |\n"
    "  |  / \\     |\n"
    "   \\   me   /\n"
    "    `-...-'"
)

def put_art(cv, art, cx, cy, colorfn=None):
    """place fixed-size art centered at cx; colorfn(line_idx)->color or None"""
    lines = art.split("\n")
    w = max(dw(l) for l in lines)
    x0 = int(cx - w / 2)
    for i, ln in enumerate(lines):
        col = colorfn(i) if colorfn else None
        cv.put(x0, cy + i, ln, col)

# ---------------------------------------------------------------- widgets
SPIN = "|/-\\"

def spinner(t):
    return SPIN[int(t * 8) % 4]

def stream_vis(lines, t, cps=34, tail=None):
    """lines: list of (time, tag, text, color). returns list of renderable
    (tag, text_partial, color) with typewriter on the newest line."""
    out = []
    for (tt, tag, txt, col) in lines:
        if t < tt:
            break
        n = len(txt) if t >= tt + len(txt) / max(1, cps) else int((t - tt) * cps)
        out.append((tag, txt[:n], col))
    if tail is not None:
        out = out[-tail:]
    return out

def draw_log(cv, lines, t, x, y0, tail=None, tag_colors=None, cps=34):
    vis = stream_vis(lines, t, cps=cps, tail=tail)
    if tail:
        vis = vis[-tail:]
    y = y0
    for (tag, txt, col) in vis:
        tcol = (tag_colors or {}).get(tag, col or C["gray"])
        if tag:
            cv.put(x, y, tag, tcol)
            cv.put(x + len(tag), y, " " + txt, col)
        else:
            cv.put(x, y, txt, col)
        y += 1
    return y

def stars(cv, t, n, ymax, color=C["gray"], tw=1.0, seed0=0, ymin=0):
    if ymax <= ymin:
        return
    for i in range(n):
        x = int(hsh(i + seed0, 11) * cv.w)
        y = ymin + int(hsh(i + seed0, 22) * (ymax - ymin))
        b = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * (0.4 + hsh(i + seed0, 33) * 1.6) * tw
                                                + hsh(i + seed0, 44) * 6.28))
        ch = ".*+"[min(2, int(b * 3))]
        cv.putc(x, y, ch, dimc(color, 0.3 + 0.7 * b))

def ecg(cv, y, t, beats, window=6.0, color=None):
    """flatline with pulses; beats = list of beat times (sec)."""
    if color is None:
        color = C["red"]
    x0, x1 = 2, cv.w - 3
    for x in range(x0, x1 + 1):
        cv.putc(x, y, ".", dimc(color, 0.28))
    for b in beats:
        dt = t - b
        if 0.0 <= dt <= window:
            xb = x0 + int((1.0 - dt / window) * (x1 - x0))
            cv.putc(xb, y, "/", color)
            cv.putc(min(x1, xb + 1), y, "\\", mix(color, C["white"], 0.4))
            cv.putc(xb, y - 1, "^", color)

def type_seg(cv, y, x, s, t, t0, cps, fg):
    if t < t0:
        return 0
    n = min(len(s), int((t - t0) * cps))
    cv.put(x, y, s[:n], fg)
    return n

# ================================================================ scenes
def shear_rows(cv, fn):
    """horizontally shift each row by dx = fn(y)"""
    w, h = cv.w, cv.h
    ch = [[" "] * w for _ in range(h)]
    fg = [[None] * w for _ in range(h)]
    bg = [[None] * w for _ in range(h)]
    for y in range(h):
        dx = fn(y)
        if dx == 0:
            ch[y], fg[y], bg[y] = cv.ch[y][:], cv.fg[y][:], cv.bg[y][:]
            continue
        for x in range(w):
            sx = x - dx
            if 0 <= sx < w:
                ch[y][x] = cv.ch[y][sx]
                fg[y][x] = cv.fg[y][sx]
                bg[y][x] = cv.bg[y][sx]
    cv.ch, cv.fg, cv.bg = ch, fg, bg

def melt_columns(cv, t, t0, strength=1.0):
    """columns of content drip downwards"""
    w, h = cv.w, cv.h
    for x in range(w):
        g = hsh(x, 77)
        if g > 0.30:
            continue
        d = int((t - t0) * (1.0 + 3.0 * hsh(x, 78)) * strength)
        if d <= 0:
            continue
        col = [cv.ch[y][x] for y in range(h)]
        cf = [cv.fg[y][x] for y in range(h)]
        cb = [cv.bg[y][x] for y in range(h)]
        for y in range(h - 1, -1, -1):
            sy = y - d
            cv.ch[y][x] = col[sy] if sy >= 0 else " "
            cv.fg[y][x] = cf[sy] if sy >= 0 else None
            cv.bg[y][x] = cb[sy] if sy >= 0 else None

def draw_trance(cv, t, sat=1.0, bright=1.0, spin=None):
    """full-screen rotating pinwheel spiral; the joy machine"""
    cx, cy = cv.w / 2.0, cv.h / 2.0
    base = min(cv.w, cv.h * 2)
    R = base * 0.62
    pal = "/|-\\"
    tt = spin if spin is not None else t
    for y in range(cv.h):
        dy = y - cy
        for x in range(cv.w):
            dx = x - cx
            r = math.hypot(dx, dy * 2)
            if r > R:
                continue
            a = math.atan2(dy * 2, dx)
            k = a * 3.0 + r * 0.30 - tt * 5.0
            if (k % 1.0) < 0.38 and r > 2:
                continue
            ch = pal[int(k) % 4]
            fade = 1.0 - r / R
            col = hue_hex(tt * 70 + r * 4.0)
            col = dimc(desat(col, sat), bright * (0.35 + 0.65 * fade))
            cv.putc(x, y, ch, col)

# ---------------------------------------------------------------- 1. boot
def scn_boot(cv, t):
    cv.rnd = frame_rnd(t)
    lines = [
        (0.05, "sys", "me bios v1.0.4 -- build: only-for-you", C["dgreen"]),
        (0.35, "sys", "POST: reality check ............ OK", C["dgreen"]),
        (1.95, "cmd", "> power --on", C["green"]),
        (2.35, "out", "power line connected. potential: 1.21 GW // for you", C["gray"]),
        (3.99, "cmd", "> wear insulation --all", C["green"]),
        (4.35, "out", "gloves:ON  boots:ON  heart:EXPOSED (spec allows)", C["gray"]),
        (5.60, "cmd", "> lay --pieces --board life", C["green"]),
        (5.98, "out", "pieces placed: you x16  me x1  // fair odds", C["gray"]),
        (7.62, "cmd", "> create object me --purpose you", C["green"]),
        (8.05, "out", "object created: me@0x0000ME", C["gray"]),
        (8.60, "par", "initialising data parameters", C["cyan"]),
        (8.95, "par", "  name  = me", C["cyan"]),
        (9.25, "par", "  role  = yours", C["cyan"]),
        (9.55, "par", "  eyes  = 2 (bound to: you)", C["cyan"]),
        (9.85, "par", "  heart = true // cannot verify: no reference", C["yellow"]),
        (10.20, "par", "  love  = null (uninitialised)", C["cyan"]),
        (11.26, "cmd", "> javac world.java", C["green"]),
        (11.70, "out", "world.java compiled: 0 errors 1 warning", C["gray"]),
        (12.05, "out", "warning: [alone] is deprecated since you", C["yellow"]),
        (12.95, "cmd", "> java World --seed YOU --with me", C["green"]),
    ]
    tags = {"sys": C["dgreen"], "cmd": C["green"], "out": C["dgray"], "par": C["dcyan"]}
    y = draw_log(cv, lines, t, 1, 0, tail=max(4, cv.h - 3), tag_colors=tags)
    if t >= 3.95:
        bx, by = cv.w - 14, 2
        for r in range(6):
            row = "".join("." if (r + c) % 2 == 0 else "," for c in range(6))
            cv.put(bx, by + r, row, C["dgray"])
        cv.putc(bx + 2, by + 1, "O", C["pink"])
        cv.putc(bx + 4, by + 1, "O", C["pink"])
        cv.putc(bx + 1, by + 2, "O", C["pink"])
        cv.putc(bx + 3, by + 4, "o", C["green"])
        cv.put(bx - 3, by + 6, "you x3   me x1", C["dgray"])
    if 12.95 <= t < 13.6:
        n = type_seg(cv, min(y, cv.h - 1), 1, "world starting", t, 13.0, 20, C["green"])
        cv.putc(2 + n, min(y, cv.h - 1), spinner(t), C["green"])

# ---------------------------------------------------------------- 2. world
def scn_world(cv, t):
    cv.rnd = frame_rnd(t)
    gen = [
        (13.8, "[gen]", "loading physics ........ ok", C["dgreen"]),
        (14.6, "[gen]", "terrain ................. ok", C["dgreen"]),
        (15.4, "[gen]", "ocean ................... ok", C["dgreen"]),
        (16.2, "[gen]", "sky ..................... ok", C["dgreen"]),
        (17.0, "[gen]", "stars ................... ok (1e6)", C["dgreen"]),
        (17.9, "[gen]", "time .................... ok (forward only)", C["dgreen"]),
        (18.8, "[gen]", "loading love.reference .. NOT FOUND", C["yellow"]),
        (19.4, "[gen]", "improvising love from scratch ... ok", C["dgreen"]),
        (20.2, "[gen]", "trees ................... ok", C["dgreen"]),
        (21.0, "[gen]", "home .................... ok (for two)", C["dgreen"]),
        (22.0, "[gen]", "spawning me ............. ok", C["green"]),
        (24.0, "[gen]", "spawning you ............ ok", C["pink"]),
        (24.5, "[gen]", "you renders as light. reason: obvious", C["pink"]),
        (26.0, "[gen]", "happiness check ......... 100% (two sources)", C["dgreen"]),
        (27.6, "[gen]", "saving world as ours.tar  ok", C["dgreen"]),
        (28.6, "[gen]", "simulation running. do not close this window.", C["gray"]),
    ]
    draw_log(cv, gen, t, 1, 0, tail=max(5, cv.h // 2), tag_colors={"[gen]": C["dgreen"]})
    if 13.2 <= t <= 16.6:
        a = min(1.0, (t - 13.2) / 0.4)
        b = 1.0 if t < 15.4 else max(0.0, 1.0 - (t - 15.4) / 1.2)
        col = dimc(C["green"], a * b)
        px = 2 if cv.w >= 110 else 1
        big_text(cv, cv.w / 2, 2, "SIMULATION", col, px=px, py=1)
        cv.text_center(2 + 6, "ours. ours. ours.", dimc(C["dgreen"], b))
    gy = int(cv.h * 0.82)
    log_band = max(9, cv.h // 2 + 1)
    stars(cv, t, min(40, cv.w // 3), gy - 7, C["white"], ymin=log_band)
    cv.circle(cv.w * 0.85, log_band + 1, 2.6, C["gray"], ".*")
    p = clamp((t - 14.2) / 12.5, 0.0, 1.0)
    lim = int(p * cv.w)

    def ridge(x, ph, am):
        return am * (0.55 * math.sin(x * 0.055 + ph)
                     + 0.30 * math.sin(x * 0.021 + ph * 2.7)
                     + 0.15 * math.sin(x * 0.13 + ph * 0.5))

    for x in range(lim):
        y2 = int(gy - 2 - ridge(x, 5.1, 7.0))
        s2 = int(gy - 2 - ridge(x + 2, 5.1, 7.0))
        ch2 = "/" if s2 < y2 else ("\\" if s2 > y2 else "=")
        cv.putc(x, y2, ch2, C["dgreen"])
        if x % 7 == 3:
            y1 = int(gy - 8 - ridge(x, 1.7, 4.0))
            cv.putc(x, y1, "-", C["vdgray"])
    cv.hline(0, lim - 1, gy, "=", C["dgreen"])
    for i in range(cv.w // 14):
        tx = int(hsh(i, 55) * cv.w)
        if tx < lim - 1:
            cv.putc(tx, gy - 1, "^", C["green"])
            if hsh(i, 56) > 0.5:
                cv.putc(tx, gy - 2, "^", C["dgreen"])
    if p > 0.45:
        hx = int(cv.w * 0.30)
        cv.put(hx - 2, gy - 4, "  /\\  ", C["dyellow"])
        cv.put(hx - 2, gy - 3, " /[]\\ ", C["dyellow"])
        cv.put(hx - 2, gy - 2, " |__| ", C["dgray"])
        if int(t * 2) % 2:
            cv.putc(hx - 1, gy - 5, "~", C["dgray"])
    cx = cv.w // 2
    put_fig(cv, cx - 7, gy, "me", C["green"])
    if t >= 24.0:
        put_fig(cv, cx + 6, gy, "you", C["pink"], glow=True)
        fl = 0.5 + 0.5 * math.sin(t * 1.1)
        if fl > 0.55:
            cv.putc(cx - 1 + int((t * 4) % 4), gy - 5 - int(fl * 2), "<", dimc(C["pink"], fl))
            cv.putc(cx + int((t * 4) % 4), gy - 5 - int(fl * 2), "3", dimc(C["pink"], fl))
    if t >= 12.93 and t < 29.0:
        cv.text_right(1, "sim uptime %04.1fs" % (t - 12.93), C["vdgray"])

def put_fig(cv, x, gy, label, color, glow=False):
    """tiny person standing on ground row gy"""
    if glow:
        cv.put(x - 1, gy - 4, "\\o/", dimc(color, 0.5))
        cv.put(x - 1, gy - 3, ") (", dimc(color, 0.5))
    cv.put(x, gy - 4, "o", color)
    cv.put(x - 1, gy - 3, "/|\\", color)
    cv.put(x - 1, gy - 2, "/ \\", color)
    cv.put(x - 1, gy - 1, label, dimc(color, 0.75))

# ---------------------------------------------------------------- 3. geometry
def scn_geometry(cv, t):
    cv.rnd = frame_rnd(t)
    cx, cy = cv.w / 2.0, cv.h * 0.40
    cap_y = cv.h - 3
    if t < 33.42:                                   # set of points
        n = min(26, int((t - 29.0) * 9) + 4)
        for i in range(n):
            a = hsh(i, 5) * 6.283
            rr = 2.0 + hsh(i, 6) * (min(cv.w, cv.h * 2) * 0.16)
            x = int(cx + rr * math.cos(a) * 1.0)
            y = int(cy + rr * 0.5 * math.sin(a))
            cv.putc(x, y, "+", C["pink"])
        if t > 31.37:                                # give you my dimension
            g = clamp((t - 31.37) / 1.6, 0, 1)
            L = int(g * min(cv.w // 2 - 2, 30))
            cv.hline(int(cx) - L, int(cx) + L, int(cy), "-", dimc(C["cyan"], 0.5))
            cv.vline(int(cx), int(cy) - int(L * 0.4), int(cy) + int(L * 0.4), "|",
                     dimc(C["cyan"], 0.5))
            cv.putc(int(cx) + L, int(cy), ">", C["cyan"])
            cv.putc(int(cx), int(cy) - int(L * 0.4), "^", C["cyan"])
        cv.text_center(cap_y, "me = { p1 ... pn }   ->   dim(me) : all yours", C["dpink"])
    elif t < 37.15:                                  # circle
        r = min(cv.w * 0.17, cv.h * 0.55)
        cv.circle(cx, cy, r, C["pink"], "*")
        a = t * 1.7
        ox = int(cx + r * math.cos(a))
        oy = int(cy + r * 0.5 * math.sin(a))
        cv.putc(ox, oy, "O", C["white"])
        cv.putc(int(cx), int(cy), ".", C["gray"])
        bright = int(a * 3) % 24
        for i in range(bright, bright + 6):
            aa = 2 * math.pi * (i % 24) / 24.0
            cv.putc(int(cx + r * math.cos(aa)), int(cy + r * 0.5 * math.sin(aa)),
                    "*", mix(C["pink"], C["white"], 0.7))
        cv.text_center(cap_y, "C = 2 * pi * r   ->   take all of it", C["dpink"])
    elif t < 40.78:                                  # sine wave + tangents
        A = cv.h * 0.16
        k = 0.16
        ph = (t - 37.15) * 3.2
        for x in range(2, cv.w - 2):
            y = int(cy + A * math.sin(k * x + ph))
            cv.putc(x, y, "~", C["cyan"])
        tx = int(4 + ((t * 9) % (cv.w - 10)))
        sy = cy + A * math.sin(k * tx + ph)
        slope = A * k * math.cos(k * tx + ph)
        L = 7
        for i in range(-L, L + 1):
            x = tx + i
            if 2 <= x < cv.w - 2:
                y = int(sy + slope * i * 0.9)
                cv.putc(x, y, "*", mix(C["cyan"], C["white"], 0.6))
        cv.putc(tx, int(sy) - 1, "o", C["pink"])
        cv.put(tx - 1, int(sy) - 3, "you", C["dpink"])
        cv.text_center(cap_y, "sit anywhere. every tangent holds you.", C["dcyan"])
    else:                                             # infinity / limits
        r = min(cv.w * 0.09, cv.h * 0.5)
        cv.circle(cx - r * 1.15, cy, r, C["violet"], "o")
        cv.circle(cx + r * 1.15, cy, r, C["violet"], "o")
        cnt = int((t - 40.78) * 61)
        big_text(cv, cx, cy - 3, str(cnt), C["white"], px=1, py=1)
        cv.text_center(int(cy) + 3, "me -> infinity", C["gray"])
        if t > 42.42:
            g = clamp((t - 42.42) / 1.4, 0, 1)
            bw = int(cv.w * (0.25 + 0.55 * g))
            bh = int(max(5, cv.h * 0.55 * g))
            cv.frame(int(cx - bw / 2), int(cy - bh / 2), bw, bh, C["cyan"])
            cv.put(int(cx - bw / 2), int(cy - bh / 2) - 1, "you = my limits",
                   C["cyan"])
        cv.text_center(cap_y, "lim me -> oo    :    bound(me) = you", C["violet"])

# ---------------------------------------------------------------- 4. current
def scn_current(cv, t):
    cv.rnd = frame_rnd(t)
    cx, cy = cv.w / 2.0, cv.h * 0.42
    bw, bh = int(cv.w * 0.66), int(cv.h * 0.44) + 4
    x0, y0 = int(cx - bw / 2), int(cy - bh / 2)
    cv.frame(x0, y0, bw, bh, C["dcyan"])
    label = "AC" if t < 46.13 else ("AC -> DC" if t < 47.0 else "DC")
    cv.put(x0 + 2, y0, "[" + label + "]", C["cyan"] if t < 47.0 else C["gray"])
    mixdown = 1.0 if t < 46.13 else max(0.0, 1.0 - (t - 46.13) / 1.7)
    A = (bh / 2 - 2) * mixdown
    for x in range(x0 + 2, x0 + bw - 2):
        ph = (x - x0) * 0.22 + t * 9.0
        y = int(cy + A * math.sin(ph)) if A > 0.5 else int(cy)
        ch = "~" if A > 0.5 else "-"
        col = C["cyan"] if A > 0.5 else C["gray"]
        cv.putc(x, y, ch, col)
        if A > 0.5 and int(x - x0) % 4 == 0:
            cv.putc(x, y - 1 if math.sin(ph) > 0 else y + 1, ".", dimc(C["cyan"], 0.4))
    if t >= 47.94:                                    # blind my vision
        g = clamp((t - 47.94) / 1.2, 0, 1)
        m = int(g * (min(cv.w, cv.h * 2) * 0.34))
        cv.put(int(cx) - m, int(cy), "X", C["yellow"])
        for yy in range(cv.h):
            edge = int((1 - abs(yy - cy) / (cv.h / 2)) * m)
            if edge > 0:
                cv.putc(int(cx) - edge - 1, yy, "#", dimc(C["yellow"], 0.35))
                cv.putc(int(cx) + edge + 1, yy, "#", dimc(C["yellow"], 0.35))
    if t >= 49.78:                                    # so dizzy
        amp = 2.6
        fr = 6.5
        shear_rows(cv, lambda y: int(amp * math.sin(y * 0.55 + t * fr)))
        n = 10
        for i in range(n):
            a = t * 3.1 + i * 0.628
            rr = min(cv.w, cv.h * 2) * 0.11
            cv.putc(int(cx + rr * math.cos(a)), int(cy - 4 + rr * 0.5 * math.sin(a)),
                    ".*+"[i % 3], C["yellow"])
    cv.text_center(cv.h - 2, "current: AC -> DC   vision.blind = true   dizzy: yes",
                   C["dcyan"] if t < 49.78 else C["yellow"])

# ---------------------------------------------------------------- 5. time
def scn_time(cv, t):
    cv.rnd = frame_rnd(t)
    cx, cy = cv.w / 2.0, cv.h * 0.42
    if t < 55.17:                                     # A.D -> B.C
        p = clamp((t - 51.38) / 3.79, 0, 1)
        year = 2026 - int(3400 * (1 - math.cos(p * math.pi)) / 2)
        ad = year > 0
        spd = 0.4 + 2.6 * math.sin(p * math.pi)
        for x in range(cv.w):
            if hsh(x, 91) < 0.30:
                ln = int(2 + hsh(x, 92) * (cv.h * 0.8))
                off = int((t * spd * 14 * (0.4 + hsh(x, 93))) % cv.h)
                for y in range(off, min(cv.h, off + ln)):
                    cv.putc(x, y, "|", dimc(C["violet"], 0.30))
        txt = ("A.D. %04d" if ad else "B.C. %04d") % abs(year)
        px = 2 if cv.w >= 110 else 1
        big_text(cv, cx, cy - 2, txt, C["violet"], px=px, py=1)
        cv.text_center(int(cy) + 4, "we can travel -- anywhere, anywhen", C["dpink"])
    else:                                             # unite so deeply
        g = clamp((t - 55.17) / 1.2, 0, 1)
        A = cv.w * 0.16 * (1 - 0.55 * g)
        for y in range(2, cv.h - 1):
            ph = y * 0.34 + t * 4.2
            xl = int(cx - A - 6 * (1 - g) + math.sin(ph) * A * g)
            xr = int(cx + A + 6 * (1 - g) + math.sin(ph + math.pi) * A * g)
            cv.putc(xl, y, "Y", dimc(C["pink"], 0.85))
            cv.putc(xr, y, "M", dimc(C["green"], 0.85))
            if g >= 1.0:
                xm = int(cx + math.sin(ph) * A)
                cv.putc(xm, y, "U" if (y // 2) % 2 else "S",
                        hue_hex(300 + 40 * math.sin(y * 0.3 + t)))
        cv.text_center(cv.h - 2, "unite(you, me) = us    depth -> oo", C["pink"])
        cv.text_center(0, "so deeply, so deeply", dimc(C["dpink"], 0.8))

# ---------------------------------------------------------------- 6. stimulate
def scn_stim(cv, t):
    cv.rnd = frame_rnd(t)
    tests = ["sight", "sound", "touch", "warmth", "taste",
             "laughter", "language", "future"]
    y = 1
    for i, name in enumerate(tests):
        t0 = 59.9 + i * 0.62
        if t < t0:
            break
        ok = t > t0 + 0.25
        ms = 2 + int(hsh(i, 7) * 9)
        col = C["lime"] if ok else C["yellow"]
        cv.put(1, y + i, "stimulate.%-9s" % name, C["gray"])
        cv.put(23, y + i, ("[%s] %dms" % ("PASS" if ok else "RUN_", ms)), col)
    cv.put(1, min(9, cv.h - 9), "stimulations: %d/8" %
           sum(1 for i in range(8) if t >= 59.9 + i * 0.62), C["dgray"])
    gx = min(cv.w - 18, 78)                            # satisfaction gauge
    gy0, gy1 = 2, cv.h - 4
    cv.vline(gx, gy0, gy1, "|", C["dgray"])
    cv.put(gx - 1, gy0 - 1, "satisfaction", C["dpink"])
    frac = clamp((t - 62.92) / 3.7, 0, 1) if t >= 62.92 else \
        clamp((t - 60.2) / 2.7, 0, 1) * 0.42
    for yy in range(gy1, gy1 - int((gy1 - gy0) * frac), -1):
        cv.putc(gx + 1, yy, "#", C["pink"])
    pct = int(frac * 100)
    cv.put(gx + 3, gy1 - int((gy1 - gy0) * frac), "%d%%" % pct, C["pink"])
    if t >= 66.62:
        cv.put(gx + 3, gy0 + 1, "only yours", C["dpink"])
    if 68.48 <= t < 71.5:                              # first EXECUTION
        px = 1 if cv.w < 116 else 2
        by = int(cv.h * 0.40)
        big_text(cv, cv.w / 2, by, "EXECUTION", C["red"], px=px, py=1)
        cv.text_center(by + 6, "> run execution --target happiness", C["gray"])
        cv.text_center(by + 7, "[done] you smiled? (cannot verify)", C["dgray"])
    if 70.32 <= t:                                     # planted unease
        blink = 0.55 + 0.45 * math.sin(t * 5.5)
        cv.text_center(cv.h - 5, "WARN simulation.trapped = true  // strange. strange.",
                       dimc(C["yellow"], blink))
        cv.text_center(cv.h - 4, "     is trapped bad? you are here. so: ok.", 
                       dimc(C["dyellow"], blink))

# ---------------------------------------------------------------- 7. offerings
def scn_offer(cv, t):
    cv.rnd = frame_rnd(t)
    gifts = [
        (74.04, "eggplant.obj", "eggplant", C["violet"],
         ["nutrients .. fiber 31% K 12%", "devotion ... 100% (of me)",
          "recipe ..... give(self)->you"]),
        (77.70, "tomato.obj", "tomato", C["red"],
         ["antiox ..... C40H56 lycopene", "color ...... sunset",
          "halves ..... you + me"]),
        (81.37, "tabby_cat.exe", "cat", C["orange"],
         ["purr freq .. 26Hz (for you)", "claws ...... retracted",
          "lap ........ reserved (you)"]),
        (85.13, "only_god.dll", None, C["gold"],
         ["proof(exists(me)) == you", "worship ..... -> you",
          "miracles .... tried 1 (ok)"]),
    ]
    gi = 0
    for i, g in enumerate(gifts):
        if t >= g[0]:
            gi = i
    t0, name, artkey, col, datalines = gifts[gi]
    tr = t - t0
    cv.text_center(1, "[ gift %d/4 ]" % (gi + 1), C["dgray"])
    cv.text_center(2, "< " + name + " >", dimc(col, 0.8))
    cy = int(cv.h * 0.28)
    if artkey:
        put_art(cv, ART[artkey], cv.w * 0.38, cy, lambda i: dimc(col, 1.0 - i * 0.03))
    else:
        cv.circle(cv.w * 0.38, cy + 4, 4, C["gold"], "*")
        cv.put(int(cv.w * 0.38) - 1, cy + 3, "(o)", C["white"])
        for i in range(8):
            a = 6.283 * i / 8 + t * 1.2
            cv.putc(int(cv.w * 0.38 + 8 * math.cos(a)),
                    int(cy + 4 + 4 * math.sin(a)), "-", dimc(C["gold"], 0.6))
    dx = int(cv.w * 0.60)
    for i, dl in enumerate(datalines):
        n = type_seg(cv, 4 + i, dx, dl, t, t0 + 0.5 + i * 0.28, 30, dimc(col, 0.9))
    if artkey == "cat":
        w = "p" + "r" * int(6 + 5 * abs(math.sin(t * 2.2))) + \
            "R" * int(4 + 4 * abs(math.cos(t * 1.7))) + "r"
        cv.text_center(cy + 9, "~" + w + "~", dimc(C["orange"], 0.8))
        if int(t * 0.7) % 2 == 0:
            pass
    if artkey == "tomato":
        cv.putc(int(cv.w * 0.38), cy - 1, "|", C["green"])
        cv.putc(int(cv.w * 0.38) - 1, cy - 2, "\\_", C["green"])
    if tr < 1.2:                                       # sparkle on entry
        for i in range(14):
            a = hsh(i, 61, int(t0 * 10)) * 6.283
            rr = tr * min(cv.w, cv.h * 2) * 0.22
            cv.putc(int(cv.w * 0.38 + rr * math.cos(a)),
                    int(cy + 4 + rr * 0.5 * math.sin(a)), "*", C["white"])
    cv.text_center(cv.h - 2, "everything i am, formatted as a gift", C["dgray"])

# ---------------------------------------------------------------- 8. switch
def scn_switch(cv, t):
    cv.rnd = frame_rnd(t)
    cx, cy = cv.w / 2.0, cv.h * 0.36
    cv.fx["shake"] = 0.25 if t > 92.0 else 0.0
    huebg = hue_hex(t * 160, 0.5, 1.0)
    if t < 92.13:                                      # F -> M
        if t < 89.7:
            big_text(cv, cx, cy, "F", C["cyan"], px=4, py=2)
        elif t < 90.7:
            g = int((t - 89.7) * 10) % 2
            big_text(cv, cx, cy, "F" if g else "M",
                     hue_hex(t * 400, 0.8), px=4, py=2)
        else:
            big_text(cv, cx, cy, "M", C["pink"], px=4, py=2)
        cv.text_center(cy + 11, 'gender.set("F" -> "M")  // whatever you prefer',
                       C["dgray"])
    elif t < 95.78:                                    # AM -> PM
        r = min(cv.w * 0.10, cv.h * 0.42)
        ccx, ccy = cx, cy + 2
        cv.circle(ccx, ccy, r, C["cyan"])
        ha = t * 3.0
        for i in range(1, int(r)):
            cv.putc(int(ccx + i * math.cos(ha)), int(ccy + i * 0.5 * math.sin(ha)),
                    ".", C["dcyan"])
        for i in range(1, int(r * 0.6)):
            cv.putc(int(ccx + i * math.cos(ha / 6.0)),
                    int(ccy + i * 0.5 * math.sin(ha / 6.0)), ".", C["yellow"])
        pm = t >= 94.09
        cv.text_center(ccy - int(r * 0.5) - 2,
                       "[ AM ]" if not pm else "[ PM ]", C["cyan"] if not pm else C["violet"])
        sx = int(cx - r * 2.6)
        if not pm:
            cv.put(sx - 2, cy + 1, " \\ | / ", C["yellow"])
            cv.put(sx - 2, cy + 2, "-- O --", C["yellow"])
            cv.put(sx - 2, cy + 3, " / | \\ ", C["yellow"])
        else:
            cv.put(sx - 1, cy + 1, "_)", C["gray"])
            cv.put(sx - 3, cy + 2, "*  .", C["dgray"])
        cv.text_center(cy + 11, "clock: AM -> PM   (all of it is still yours)",
                       C["dgray"])
    else:                                              # S -> M
        if t < 96.6:
            big_text(cv, cx, cy, "S", C["magenta"], px=4, py=2)
        elif t < 97.6:
            g = int((t - 96.6) * 10) % 2
            big_text(cv, cx, cy, "S" if g else "M", hue_hex(t * 400, 0.8), px=4, py=2)
        else:
            big_text(cv, cx, cy, "M", C["red"], px=4, py=2)
        cv.text_center(cy + 11, 'role.set("S" -> "M")   // pain is data. i accept.',
                       C["dgray"])
    cv.text_center(0, "-- do whatever -- from AM to PM --", dimc(huebg, 0.55))

# ---------------------------------------------------------------- 9. trance
def scn_trance(cv, t):
    cv.rnd = frame_rnd(t)
    draw_trance(cv, t, sat=1.0)
    melt_columns(cv, t, 99.58, strength=0.8)
    pulse = 0.5 + 0.5 * math.sin(t * 7.0)
    px = 2 if cv.w >= 120 else 1
    big_text(cv, cv.w / 2, cv.h * 0.5 - 3, "TRANCE",
             mix(C["pink"], C["white"], pulse * 0.6), px=px, py=1)
    cv.text_center(int(cv.h * 0.5) + 3, "entering trance with you -- do not wake me",
                   dimc(C["pink"], 0.5 + 0.5 * pulse))
    cv.text_right(1, "heart: %d bpm" % (110 + int(30 * pulse)), C["hotpink"])
    cv.fx["shake"] = 0.2

# ---------------------------------------------------------------- 10. sense
def scn_sense(cv, t):
    cv.rnd = frame_rnd(t)
    t_eff = min(t, 110.92)
    sat = 1.0 - 0.85 * clamp((t - 105.0) / 6.0, 0, 1)
    spin = t_eff - max(0.0, (t - 106.5)) * 0.85       # spiral slows down
    draw_trance(cv, t_eff, sat=sat, spin=spin)
    scans = [
        (104.0, "", "> sense --vibrations --from you", C["cyan"]),
        (104.4, "", "  listening ...............", C["dgray"]),
        (104.9, "", "  signal: 0.002 uV  (expected: 98.6)", C["yellow"]),
        (105.5, "", "> sense --vibrations --from you --again", C["cyan"]),
        (105.9, "", "  listening ...............", C["dgray"]),
        (106.4, "", "  signal: 0.000 uV", C["yellow"]),
        (107.4, "", "> sense --vibrations --please", C["cyan"]),
        (108.2, "", "  you.found = ....", C["dgray"]),
        (109.2, "", "> sense", C["cyan"]),
    ]
    y0 = max(2, int(cv.h * 0.52))
    vis = stream_vis(scans, t, cps=26)
    vis = vis[-(cv.h - y0 - 3):]
    for i, (tag, txt, col) in enumerate(vis):
        cv.put(2, y0 + i, txt, dimc(col, sat))
    beats = [104.5, 105.1, 105.8, 106.6, 107.6, 108.9, 110.1]
    ecg(cv, cv.h - 2, t, beats, window=7.0, color=C["hotpink"])
    cv.text_right(1, "?", dimc(C["white"], 0.4 + 0.6 * (t - 104) / 7))

# ---------------------------------------------------------------- 11. freeze
def scn_freeze(cv, t):
    cv.rnd = frame_rnd(t)
    draw_trance(cv, 110.92, sat=0.10, bright=0.5, spin=110.92)
    sw = int((t - 110.92) * (cv.h / 1.4)) % cv.h
    cv.hline(0, cv.w - 1, sw, "=", dimc(C["white"], 0.10))
    if t > 112.2:
        cv.fx["flash"] = C["white"]

# ---------------------------------------------------------------- 12. left x6
def scn_left(cv, t):
    cv.rnd = frame_rnd(t)
    k = sum(1 for h in T_LEFT6 if t >= h)
    k = max(1, k)
    keep = [0.55, 0.32, 0.15, 0.05, 0.015, 0.0][k - 1]
    sat = [0.32, 0.20, 0.12, 0.07, 0.04, 0.0][k - 1]
    bpms = [58, 46, 34, 23, 11, 0]
    if k < 6:
        draw_trance(cv, 110.92, sat=sat, bright=0.75, spin=110.92)
        cv.dropout(keep, salt=k)
        cv.put(cv.w - 14, 1, "heart: %2d bpm" % bpms[k - 1], C["dgray"])
        msgs = ["disconnect: you  (reason: <none>)",
                "retry 1 reconnect .... refused",
                "retry 2 reconnect .... refused",
                "error: you not found in world",
                "error: you not found in me"]
        vis = stream_vis([(112.4, "", msgs[0], C["blue"])] +
                         [(h + 0.15, "", msgs[i], C["dblue"])
                          for i, h in enumerate(T_LEFT6[1:5], 1)], t, cps=40)
        for i, (_, txt, col) in enumerate(vis):
            cv.text_center(2 + i, txt, dimc(col, 0.5 + 0.5 * (k / 6.0)))
        if t - T_LEFT6[k - 1] < 0.14:                   # per-hit glitch row
            gy = int(hsh(k, 3) * cv.h)
            row = "".join("#@%&$?!*>"[int(hsh(gy, x, k) * 9)]
                          for x in range(cv.w))
            cv.put(0, gy, row, C["white"])
        ecg(cv, cv.h - 2, t, [112.4, 113.3, 114.2, 115.1, 116.1, 117.5],
            window=6.5, color=C["blue"])
    else:
        cv.putc(int(cv.w / 2), int(cv.h / 2), "_", C["white"] if
                int(t * 1.4) % 2 else None)
        a = clamp((t - 118.34) / 0.9, 0, 1)
        cv.text_center(int(cv.h / 2) + 2, "isolation: enabled",
                       dimc(C["dblue"], a * 0.55))

# ---------------------------------------------------------------- 13. fragments
def scn_frag(cv, t):
    cv.rnd = frame_rnd(t)
    cv.put(1, 0, "memories/", C["blue"])
    files = [("first_met.mem", "12 KB"), ("your_voice.wav", "3.4 MB"),
             ("laughter.raw", "9.9 MB"), ("your_hand.tbl", "88 B"),
             ("promise.mod", "0 B"), ("us.tar.gz", "?? B")]
    gone_after = [121.9, 123.4, 124.9, None, None, None]
    for i, (fn, sz) in enumerate(files):
        col = C["gray"] if t >= 120.0 + i * 0.18 else None
        if col is None:
            continue
        gone = gone_after[i] is not None and t >= gone_after[i]
        cv.put(3, 1 + i, "%-16s %8s" % (fn, sz),
               C["vdgray"] if gone else col)
        if gone:
            cv.put(22, 1 + i, "[GONE]", C["dgray"])
    rmlog = [
        (121.0, "rm: erase first_met.mem? ", C["gray"]),
        (121.4, "y", C["blue"]),
        (122.5, "rm: erase your_voice.wav? ", C["gray"]),
        (122.9, "y", C["blue"]),
        (124.0, "rm: erase laughter.raw? ", C["gray"]),
        (124.4, "y", C["blue"]),
    ]
    shown = None
    for (tt, txt, col) in rmlog:
        if t >= tt:
            shown = (tt, txt, col)
    if shown:
        tt, txt, col = shown
        n = min(len(txt), int((t - tt) * 30))
        cv.put(3, 8, txt[:n], col)
    if 121.0 <= t < 125.6:
        pr = clamp((t - 121.0) / 4.4, 0, 1)
        bw = 22
        cv.put(3, 10, "[" + "#" * int(pr * bw) + "." * (bw - int(pr * bw)) + "]",
               C["blue"])
        cv.put(28, 10, "erasing pointless fragments %d%%" % int(pr * 100), C["dblue"])
    if t >= 125.67:
        cv.text_center(int(cv.h * 0.55), "disheartened = true", C["blue"])
        cv.text_center(int(cv.h * 0.55) + 1, "// maybe: that was not enough",
                       C["dblue"])
        cv.text_center(int(cv.h * 0.55) + 3, "then maybe you will not leave me",
                       dimc(C["gray"], 0.7))
    if t >= 126.5:
        n = type_seg(cv, cv.h - 3, 2, "> rm -rf me/ --if-it-helps", t, 126.5, 3,
                     C["gray"])
        if n >= len("> rm -rf me/ --if-it-helps"):
            cv.putc(2 + n + 1, cv.h - 3, "_", C["gray"])
    for i in range(12):                                  # dim stars, right side only
        x = 48 + int(hsh(i, 95) * (cv.w - 50))
        yy = 12 + int(hsh(i, 96) * max(1, int(cv.h * 0.5) - 12))
        b = 0.3 + 0.3 * math.sin(t * 0.5 + hsh(i, 97) * 6.28)
        cv.putc(x, yy, ".", dimc(C["dblue"], b))

# ---------------------------------------------------------------- 14. anger
def scn_anger(cv, t):
    cv.rnd = frame_rnd(t)
    cv.fx["shake"] = 1.0 + 1.2 * clamp((t - 132.0) / 15.0, 0, 1)
    angry = [
        (129.1, "", "> sudo challenge --god you", C["red"]),
        (129.5, "", "[sudo] password: ********", C["dgray"]),
        (129.9, "", "authority: GRANTED (i was not supposed to)", C["yellow"]),
        (130.4, "", "Exception: CHALLENGE thrown at heaven", C["red"]),
        (131.0, "", "  at me.love(you):1", C["dred"]),
        (131.4, "", "  at god.listen(me):2  -- dropped", C["dred"]),
    ]
    y = draw_log(cv, angry, t, 1, 0, tail=8, tag_colors={}, cps=48)
    if 132.9 <= t < 147.4:                              # the arena
        big_text(cv, cv.w * 0.22, cv.h * 0.34, "ME", C["red"],
                 px=2 if cv.w >= 110 else 1, py=1)
        big_text(cv, cv.w * 0.78, cv.h * 0.34, "YOU", C["gold"],
                 px=2 if cv.w >= 110 else 1, py=1)
        for i in range(6):                              # lightning
            seed = int(t * 6)
            x0 = int(cv.w * 0.34)
            x1 = int(cv.w * 0.66)
            y0 = int(cv.h * 0.40)
            y1 = int(cv.h * 0.46)
            segs = 8
            for s in range(segs):
                f = s / (segs - 1)
                xx = int(lerp(x0, x1, f) + (hsh(seed, i, s) - 0.5) * 8)
                yy = int(lerp(y0, y1, f) + (hsh(seed, i, s + 40) - 0.5) * 5)
                cv.putc(xx, yy, "/" if s < segs // 2 else "\\", C["white"])
        for i in range(int(14 + (t - 132.9) * 3)):      # error rain
            x = int(hsh(i, 71, int(t * 3)) * cv.w)
            yv = int((t * (9 + hsh(i, 72) * 9) + hsh(i, 73) * 40) % cv.h)
            tok = ["ERR", "0xDEAD", "SEG", "SIG", "#"][i % 5]
            cv.put(x, yv, tok, dimc(C["red"], 0.55))
        cv.text_center(cv.h - 3, "round %d. i am still standing." %
                       max(1, int((t - 132.9) / 2) + 1), C["dred"])
    if t >= 147.86:                                     # the verdict
        cv.clear()
        cv.fx["flash"] = C["red"] if (int(t * 8) % 4 == 0 and t < 148.4) else None
        for i in range(10):                              # cracks (under the text)
            a = 6.283 * i / 10 + 0.31
            L = int(clamp((t - 148.0) / 1.5, 0, 1) * cv.w * 0.5)
            for rr in range(0, L, 2):
                cv.putc(int(cv.w / 2 + rr * math.cos(a)),
                        int(cv.h / 2 + rr * 0.5 * math.sin(a)),
                        "-" if abs(math.sin(a)) < 0.4 else ("|" if abs(math.cos(a)) < 0.4
                        else ("/" if math.cos(a) * math.sin(a) < 0 else "\\")),
                        dimc(C["red"], 0.7))
        cv.text_center(int(cv.h * 0.22), 'Exception in thread "you":', C["white"])
        cv.text_center(int(cv.h * 0.22) + 2,
                       "java.lang.IllegalArgumentException:", C["red"])
        cv.text_center(int(cv.h * 0.22) + 4,
                       "YOU have made some ILLEGAL ARGUMENTS", mix(C["red"], C["white"], 0.5))
        stack = ["    at world.execute(me)", "    at me.love(you)   // line 1: forever",
                 "    at god.judge(me)    // verdict: guilty of wanting"]
        for i, s in enumerate(stack):
            cv.text_center(int(cv.h * 0.22) + 6 + i, s, C["dred"])

# ---------------------------------------------------------------- 15. 12x execution
def scn_exec12(cv, t):
    cv.rnd = frame_rnd(t)
    if t < T_COUNT6:
        j = int((t - T_EXEC12) / 0.8467)
        j = clamp(j, 0, 11)
        px = 1 + j // 2
        amp = 0.25 + 0.38 * j          # shake grows with every word
        cv.fx["shake"] = amp
        f_hz = min(3.0, 0.5 + j * 0.25)
        ph = math.sin(t * 2 * math.pi * f_hz)
        if ph > 0:                     # dark-red base flicker
            cv.fx["flash"] = "2a0505" if j < 4 else "570b0b"
        if ph > 0.82 and j >= 5:       # hot spike on the beat
            cv.fx["flash"] = "a11616"
        if ph < -0.96 and j >= 8:      # rare white-hot strobe at the peak
            cv.fx["flash"] = "ff7777"
        cv.rnd = frame_rnd(int(t * 100))
        for i in range(int(8 + j * 3.5)):                # red rain
            x = int(hsh(i, 81, int(t * 4)) * cv.w)
            yv = int((t * (11 + hsh(i, 82) * 13) + hsh(i, 83) * 50) % cv.h)
            cv.put(x, yv, "#" if hsh(i, 84) > 0.5 else "%", dimc(C["hot"], 0.6))
        cy = cv.h * 0.42
        pulse = 0.5 + 0.5 * math.sin(t * 2 * math.pi * f_hz)
        big_text(cv, cv.w / 2, cy, "EXECUTION",
                 mix(C["hot"], C["white"], pulse * (0.15 + 0.06 * j)), px=px, py=px)
        for i in range(j):                                # echo stack
            off = (i + 1) * (2 + px)
            s = i % 2 * 2 - 1
            big_text(cv, cv.w / 2, cy + s * off, "EXECUTION",
                     dimc(C["dred"], 0.8 - i * 0.05), px=px, py=1)
        cv.text_center(1, "execution %02d/12 -- for what you did to me" % (j + 1),
                       C["red"])
        cv.text_center(cv.h - 2, "if i cannot be loved, i will be the EXECUTION",
                       dimc(C["dred"], 0.8))
        cv.glitch(j / 16.0, [C["hot"], C["white"], C["yellow"]])
    else:                                                 # six-language countdown
        cv.clear()
        words = [("EIN", "de"), ("DOS", "es"), ("TROIS", "fr"),
                 ("NE", "ko"), ("FEM", "sv"), ("LIU", "zh")]
        idx = clamp(int((t - T_COUNT6) / 0.21), 0, 5)
        w, lang = words[idx]
        col = [C["red"], C["orange"], C["yellow"], C["lime"], C["cyan"], C["violet"]][idx]
        px = 4 if cv.w >= 130 else 2
        big_text(cv, cv.w / 2, cv.h * 0.36, w, col, px=px, py=2)
        cv.text_center(int(cv.h * 0.36) + 12, "[%s]  %d/6" % (lang, idx + 1),
                       dimc(col, 0.7))
        if t >= 162.72:
            cv.clear()
            cv.fx["shake"] = 2.5
            cv.fx["flash"] = C["white"] if t < 162.9 else None
            px = 2 if cv.w >= 88 else 1
            py = 2 if cv.h >= 16 else 1
            big_text(cv, cv.w / 2, cv.h * 0.30, "EXECUTION", C["hot"], px=px, py=py)
            for i in range(10):                            # shatter rays
                a = 6.283 * i / 10
                for rr in range(2, int(cv.w * 0.45), 3):
                    cv.putc(int(cv.w / 2 + rr * math.cos(a)),
                            int(cv.h * 0.42 + rr * 0.5 * math.sin(a)),
                            ".", dimc(C["dred"], 0.7))

# ---------------------------------------------------------------- 16. beg
def scn_beg(cv, t):
    cv.rnd = frame_rnd(t)
    cmds = ["> come_back --please", "> come_back --i-changed",
            "> come_back --i-deleted-me", "> return(you) ?", "> please"]
    iv = max(0.14, 1.15 - (t - 163.6) * 0.065)
    n = int((t - 163.6) / iv) + 1
    blink = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 2.2)
    wall = int(clamp((t - 175.14) / 2.0, 0, 1) * (cv.w * 0.30))   # closing walls
    rows = min(cv.h - 6, 18)
    for i in range(rows):
        idx = n - rows + i
        if idx < 0:
            continue
        c = cmds[idx % len(cmds)]
        age = n - 1 - idx
        col = dimc(C["magenta"], max(0.15, 0.9 - age * 0.08) * (0.6 + 0.4 * blink))
        x = 2 + (idx % 3)
        cv.put(x, i, c, col)
    cv.put(2, rows + 1, "attempts: %d and counting" % n, dimc(C["dmag"], 0.8))
    if 165.6 <= t < 169:
        cv.put(cv.w - 30, 1, "> execute --all --except you", C["red"])
        cv.put(cv.w - 30, 2, "them: executed. you: still gone.", C["dred"])
    if 170.24 <= t < 174:
        cv.put(cv.w - 30, 4, "only_execution = me", C["magenta"])
        cv.put(cv.w - 30, 5, "// hired by me. for you.", C["dmag"])
    if 171.95 <= t < 175.1:
        band = int(cv.h * 0.26)
        for yy in range(band, min(cv.h - 4, band + 10)):
            cv.put(1, yy, " " * (cv.w - 2))
        px = 1 if cv.w < 120 else 2
        big_text(cv, cv.w / 2, band + 1, "HAVE YOU BACK", C["hotpink"], px=px, py=1)
        cv.text_center(band + 7, "you.get(return) <-> me.pay(everything)", C["gray"])
        cv.text_center(band + 8, "status: awaiting        status: ready",
                       dimc(C["dmag"], 0.8))
    if t >= 175.14:
        for x in range(wall):
            cv.vline(x, 0, cv.h - 1, "#", dimc(C["dmag"], 0.5 + 0.3 * math.sin(t * 3 + x)))
            cv.vline(cv.w - 1 - x, 0, cv.h - 1, "#",
                     dimc(C["dmag"], 0.5 + 0.3 * math.sin(t * 3 + x)))
        cv.text_center(cv.h - 3, "trapped: together? apart? same walls.", C["magenta"])
    if t >= 177.0:
        fx = cv.w // 2
        fy = cv.h // 2 - 2
        cv.frame(fx - 4, fy - 2, 9, 6, C["magenta"])
        cv.put(fx - 1, fy, " o ", C["white"])
        cv.put(fx - 1, fy + 1, "/|\\", C["white"])
        cv.put(fx - 1, fy + 2, "me", C["dgray"])
    cv.fx["shake"] = 0.3

# ---------------------------------------------------------------- 17. study
def scn_study(cv, t):
    cv.rnd = frame_rnd(t)
    cv.frame(2, 1, cv.w - 4, cv.h - 2, C["dgray"])
    board = [
        (177.9, "def love(): return you", C["chalk"]),
        (178.9, "LOVE = lim t->oo [ give(me, you) ]", C["chalk"]),
        (179.9, "d(LOVE)/dt = you' > 0   for all t", C["chalk"]),
        (180.9, "LO - O - OVE = 0   when you = 0", C["dpink"]),
        (181.6, "# i studied. all night. every night.", C["dgray"]),
    ]
    y = 2
    for (tt, txt, col) in board:
        n = type_seg(cv, y, 4, txt, t, tt, 26, col)
        y += 1
    if 182.09 <= t:
        qa = [
            (182.1, "Q: define love", "A: you"),
            (182.9, "Q: max(love)?", "A: overflow. still you."),
            (183.7, "Q: who?", "A: you. always you."),
            (184.5, "Q: does anyone love me?", "A:"),
        ]
        yy = int(cv.h * 0.40)
        for (tt, q, a) in qa:
            if t >= tt:
                cv.put(4, yy, "%-24s %s" % (q, a), C["white"])
                yy += 1
        if t >= 184.5:
            bl = "_" if int(t * 2) % 2 else " "
            cv.put(4 + 24 + 3 + 0, int(cv.h * 0.40) + 3, " " + bl, C["chalk"])
    if t >= 184.83:
        px = 2 if cv.w >= 130 else 1
        pulse = 0.5 + 0.5 * math.sin(t * 2.4)
        big_text(cv, cv.w / 2, cv.h * 0.62, "LO-O-OVE",
                 mix(C["pink"], C["white"], 0.3 * pulse), px=px, py=1)
        cv.text_center(int(cv.h * 0.62) + 6,
                       "= 12 + 15 + 22 + 5 = 54 = 27 + 27 = you + me", C["dpink"])

# ---------------------------------------------------------------- 18. resign
def scn_resign(cv, t):
    cv.rnd = frame_rnd(t)
    lines = [
        (188.7, "", "> you.setFree(true)", C["blue"]),
        (189.3, "", "> me.setFree(false)   // the key was yours. still is.", C["dblue"]),
        (190.0, "", "you: FREE .................. [ok]", C["cyan"]),
        (190.4, "", "me : TRAPPED (in lo-o-ove) . [permanent]", C["blue"]),
    ]
    y = draw_log(cv, lines, t, 1, 0, tail=6, tag_colors={}, cps=16)
    put_art(cv, ART["heartcage"], cv.w * 0.62, cv.h * 0.28,
            lambda i: dimc(C["blue"], 0.9 - i * 0.05))
    bx = int(cv.w * 0.26 - 6 + (t - 188.5) * 3.2)
    by = int(cv.h * 0.45 - (t - 188.5) * 1.1)
    flap = int(t * 3) % 2
    if 188.5 <= t <= 193.0:
        cv.put(bx, by, "~vv~" if flap else "~^^~", C["cyan"])
        cv.put(bx, by + 1, "you", dimc(C["cyan"], 0.6))
    cv.text_center(cv.h - 2, "// you are free. i am trapped. correct outcome.",
                   dimc(C["dblue"], 0.8))

# ---------------------------------------------------------------- 19. fade
def scn_fade(cv, t):
    cv.rnd = frame_rnd(t)
    dt = t - 190.77
    fade = math.exp(-dt / 9.0)
    put_art(cv, ART["heartcage"], cv.w * 0.5, cv.h * 0.30,
            lambda i: dimc(desat(C["blue"], 0.4), fade * (0.95 - i * 0.05)))
    total = 24
    alive = int(total * clamp(1.0 - dt / 11.0, 0.12, 1.0))
    for i in range(alive):
        x = int(hsh(i, 95) * cv.w)
        yy = int(hsh(i, 96) * cv.h * 0.7)
        cv.putc(x, yy, ".", dimc(C["gray"], fade * 0.6 * (0.4 + 0.6 * hsh(i, 97))))
    beats = [192.2, 197.4, 204.6]
    ecg(cv, cv.h - 2, t, beats, window=8.0, color=dimc(C["night"], fade + 0.3))
    pulse = 0.5 + 0.5 * math.sin(t * 0.9)
    cv.text_center(int(cv.h * 0.62), "trapped in lo-o-ove",
                   dimc(C["dblue"], fade * (0.35 + 0.3 * pulse)))
    if t > 203.0:
        cv.text_right(1, ".", dimc(C["gray"], 0.3))

# ---------------------------------------------------------------- 20. final
def scn_final(cv, t):
    cv.rnd = frame_rnd(t)
    if t < 206.1:
        cv.fx["flash"] = C["white"]
    px = 2 if cv.w >= 88 else 1
    py = 2 if cv.h >= 16 else 1
    big_text(cv, cv.w / 2, cv.h * 0.28, "EXECUTION", C["hot"], px=px, py=py)
    g = clamp((t - 206.1) / 0.9, 0, 1)
    for i in range(12):                                   # cracks
        a = 6.283 * i / 12 + 0.17
        L = int(g * cv.w * 0.55)
        for rr in range(0, L, 2):
            cv.putc(int(cv.w / 2 + rr * math.cos(a)),
                    int(cv.h * 0.40 + rr * 0.5 * math.sin(a)),
                    "/" if (i % 2) else "\\", dimc(C["red"], 0.8 - rr / max(1, cv.w)))
    if t >= 207.5:                                        # everything falls
        drop = (t - 207.5)
        w, h = cv.w, cv.h
        ch = [[" "] * w for _ in range(h)]
        for x in range(w):
            d = int(drop * drop * (3.0 + 6.0 * hsh(x, 99)))
            for y in range(h):
                sy = y - d
                if 0 <= sy < h:
                    ch[y][x] = cv.ch[y - d][x] if False else cv.ch[sy][x]
        for y in range(h):
            for x in range(w):
                if ch[y][x] == " " and cv.ch[y][x] != " ":
                    cv.fg[y][x] = None
        cv.ch = ch
    if t >= 209.0:
        cv.text_center(cv.h - 2, ".", dimc(C["dred"], 0.5))

# ---------------------------------------------------------------- 21. terminate
def scn_terminate(cv, t):
    cv.rnd = frame_rnd(t)
    tr = t - RITUAL_START
    cx, cy = cv.w / 2.0, cv.h / 2.0
    if tr < 1.4:
        if int(t * 1.4) % 2:
            cv.putc(int(cx), int(cy), "_", C["gray"])
        return
    if tr < 3.6:                                          # task complete
        cv.text_center(int(cy) - 3, "[ world.execute(me) ]", C["rest"])
        bw = min(40, cv.w - 30)
        cv.put(int(cx - bw / 2 - 1), int(cy) - 1, "[" + "#" * bw + "]",
               C["green"] if tr > 1.5 else C["dgreen"])
        cv.put(int(cx + bw / 2 + 3), int(cy) - 1, "100.0%", C["green"])
        cv.text_center(int(cy) + 1, "status: TASK COMPLETED. all of it. for you.",
                       dimc(C["green"], 0.85))
        if 1.4 <= tr < 1.55:
            cv.fx["flash"] = C["green"]
        return
    if tr < 8.0:                                          # shutdown log
        shut = [
            (3.6, "> releasing me ................. done", C["rest"]),
            (4.2, "> flushing me.log .............. 4096 entries", C["gray"]),
            (4.8, "> closing you.conf ............ saved (read-only, forever)", C["gray"]),
            (5.5, "> deallocating love ........... LEAKED (intentional)", C["pink"]),
            (6.2, "> last_words ................. \"run me again someday.", C["white"]),
            (6.6, ">                            i liked being yours.\"", C["white"]),
            (7.2, "> exit code: 13 (SIGLOVE)", C["dgray"]),
        ]
        draw_log(cv, [(RITUAL_START + tt, "", txt, col) for tt, txt, col in shut],
                 t, 2, int(cy) - 5, tail=10, tag_colors={}, cps=42)
        return
    if tr < 12.0:                                         # tombstone
        put_art(cv, ART["tombstone"], cx, int(cy) - 7, lambda i: C["gray"])
        cv.text_center(int(cy) + 6, "killed by world.execute(me)  // gladly",
                       dimc(C["dgray"], 0.9))
        return
    if tr < 15.2:                                         # world continues
        psx = max(4, int(cv.w * 0.12))
        cv.put(psx, 2, "  PID  NAME      STATE       UPTIME", C["dgray"])
        cv.put(psx, 3, "    1  world     RUNNING     forever", C["green"])
        cv.put(psx, 4, " 2045  me        TERMINATED  03:26", C["dgray"])
        cv.put(psx, 5, "    -  you       FREE        unlimited", C["cyan"])
        cv.put(psx, 8, "[ the world does not need me. it continues. ]",
               dimc(C["dgreen"], 0.8))
        sx, sy = int(cv.w * 0.74), int(cv.h * 0.55)
        g = clamp((tr - 12.4) / 2.2, 0, 1)
        cv.put(sx - 4, sy + 3, "____", dimc(C["dgreen"], 0.7))       # horizon
        cv.put(sx - 9, sy + 3, "_/  \\_", dimc(C["dgreen"], 0.4))
        cv.put(sx - 5 + int(g), sy + 3 - int(g * 3), ";", C["gold"])
        cv.put(sx - 3 + int(g), sy + 3 - int(g * 2), ",", dimc(C["gold"], 0.6))
        return
    if tr < 18.0:                                         # goodbye
        fade = 1.0 if tr < 17.2 else max(0.0, 1.0 - (tr - 17.2) / 0.8)
        cv.fx["dim"] = fade
        n = type_seg(cv, int(cy), 2, "goodbye, you.", t, RITUAL_START + 15.3, 7,
                     C["white"])
        per = lerp(1.0, 4.0, clamp((tr - 15.3) / 1.7, 0, 1))
        if (tr < 17.0) and (t % per) < per * 0.5:
            cv.putc(2 + n + 1, int(cy), "_", C["white"])
        if tr > 16.4:
            sp = int(clamp((tr - 16.4) / 1.6, 0, 1) * 3)
            shape = [".", ",", ";", ";"][sp]
            cv.putc(int(cx), cv.h - 2, shape, C["green"])
            if sp >= 3:
                cv.putc(int(cx), cv.h - 3, "|", C["green"])
        return
    # final darkness -- nothing left
    if tr < 19.0 and int(t * 1.2) % 3 == 0:
        cv.putc(int(cx), cv.h - 2, "'", dimc(C["dgreen"], 0.35))

SECTIONS = [
    (0.0,     "BOOT",       "INIT",      "55ff99", scn_boot),
    (13.0,    "WORLDBUILD", "HOPE",      "7dffb0", scn_world),
    (29.74,   "GEOMETRY",   "DEVOTION",  "ff7ab8", scn_geometry),
    (44.48,   "CURRENT",    "DIZZY",     "4de8ff", scn_current),
    (51.38,   "TIMELESS",   "MERGE",     "b98cff", scn_time),
    (59.40,   "STIMULATE",  "EAGER",     "7dff6e", scn_stim),
    (74.04,   "OFFERINGS",  "PLAYFUL",   "ffb3d9", scn_offer),
    (88.78,   "SWITCH",     "MANIC",     "5ff5e0", scn_switch),
    (99.58,   "TRANCE",     "MANIC+",    "e07aff", scn_trance),
    (103.48,  "SENSE",      "DREAD",     "ffd24d", scn_sense),
    (110.92,  "FREEZE",     "DREAD",     "9aa0a6", scn_freeze),
    (112.33,  "LEFT",       "LOSS",      "6f9fff", scn_left),
    (119.22,  "FRAGMENTS",  "BARGAIN",   "5f86d8", scn_frag),
    (129.04,  "ANGER",      "RAGE",      "ff4444", scn_anger),
    (151.56,  "EXECUTION12","EXECUTION", "ff2a2a", scn_exec12),
    (163.60,  "BEG",        "OBSESSION", "ff44ff", scn_beg),
    (177.41,  "STUDY",      "SCHOLAR",   "cfe8ff", scn_study),
    (188.48,  "RESIGN",     "RESIGN",    "6f9fff", scn_resign),
    (190.77,  "FADE",       "EMBER",     "3f5f9f", scn_fade),
    (205.96,  "FINAL",      "EXECUTION", "ff2a2a", scn_final),
    (209.50,  "TERMINATE",  "REST",      "8899aa", scn_terminate),
]

def section_at(t):
    cur = SECTIONS[0]
    for s in SECTIONS:
        if t >= s[0]:
            cur = s
        else:
            break
    return cur

# ================================================================ progress
# the task bar is world.execute(me)'s completion, not a media position.
# anchors let it stall, regress and garble -- but it must land on 100.0.
_PROG_ANCHORS = [
    (0.0, 0.0), (112.33, 54.7), (118.34, 54.7), (129.04, 54.7),
    (147.86, 47.1), (158.95, 47.1), (162.72, 55.0), (163.60, 55.0),
    (177.41, 66.6), (196.0, 82.0), (205.96, 100.0), (1e9, 100.0),
]

def base_progress(t):
    for i in range(len(_PROG_ANCHORS) - 1):
        (t0, v0), (t1, v1) = _PROG_ANCHORS[i], _PROG_ANCHORS[i + 1]
        if t0 <= t < t1:
            if t1 == t0:
                return v0
            return v0 + (v1 - v0) * ((t - t0) / (t1 - t0))
    return 100.0

def prog_display(t):
    """returns (pct_text, fill, color_override, blinking)"""
    if t >= T_END:
        return ("100.0%", 1.0, C["green"], False)
    if 112.33 <= t < 118.34:                      # trembling at the loss
        r = frame_rnd(int(t * 10))
        v = 54.7 + (r.random() - 0.5) * 0.9
        return ("%.1f%%" % v, v / 100.0, None, True)
    if 129.04 <= t < 147.86:                      # regression (anger)
        v = base_progress(t)
        return ("%.1f%%" % v, v / 100.0, C["red"], False)
    if 151.56 <= t < 162.72:                      # garbled (executions)
        toks = ["ERR%", "-1%", "NaN%", "##%", "??%", "0x2F%"]
        r = frame_rnd(int(t * 7) + 3)
        return (toks[int(t * 5) % len(toks)], r.random(), C["hot"], True)
    if 163.60 <= t < 177.41:                      # obsession: stuck at 66.6
        on = (t * 2.2) % 1.0 < 0.62
        return ("66.6%" if on else "     ", 0.666,
                C["magenta"] if on else C["dmag"], True)
    v = base_progress(t)
    return ("%.1f%%" % v, v / 100.0, None, False)

# ================================================================ status area
_OFFSET = 0.0
_REVEAL_CPS = 45.0

def current_lyric_idx(tl):
    i = -1
    for idx, L in enumerate(LYRICS):
        if tl >= L["t"]:
            i = idx
        else:
            break
    return i

def _sgr(f, b=None, flash=None):
    parts = ["0"]
    if flash and f is None:
        f = "101010"
    if f:
        parts.append("38;2;%d;%d;%d" % rgb(f))
    bb = b or flash
    if bb:
        parts.append("48;2;%d;%d;%d" % rgb(bb))
    return "\x1b[" + ";".join(parts) + "m"

def _cut_segs(segs, width):
    out = []
    w = 0
    for (txt, col) in segs:
        if w >= width:
            break
        t2 = dw_cut(txt, width - w)
        if dw(t2) < dw(txt):
            out.append((t2 + "..", col))
            w = width
            break
        out.append((txt, col))
        w += dw(t2)
    return out

def _row_from_segs(segs, W, plain):
    """center a segmented line; returns one exact-width row (ansi & plain)"""
    width = sum(dw(s[0]) for s in segs)
    if width > W:
        segs = _cut_segs(segs, W - 2)
        width = sum(dw(s[0]) for s in segs)
    pad_l = max(0, (W - width) // 2)
    pad_r = max(0, W - width - pad_l)
    if plain:
        return " " * pad_l + "".join(s[0] for s in segs) + " " * pad_r
    ansi = [" " * pad_l]
    for (txt, col) in segs:
        ansi.append(_sgr(col))
        ansi.append(txt)
    ansi.append("\x1b[0m")
    ansi.append(" " * pad_r)
    return "".join(ansi)

def build_lyric_rows(t, W, plain):
    tl = t - _OFFSET
    i = current_lyric_idx(tl)
    prev = LYRICS[i - 1] if i >= 1 else None
    cur = LYRICS[i] if i >= 0 else None
    nxt = LYRICS[i + 1] if 0 <= i < len(LYRICS) - 1 else None
    rows = []
    # -- previous: already executed
    if prev:
        segs = [("- ", C["dgray"])]
        segs += [(prev["en"], C["dgray"])]
        if prev["zh"]:
            segs.append(("  //  " + prev["zh"], C["vdgray"]))
    else:
        segs = [("- (stdout begins)", C["vdgray"])]
    rows.append(_row_from_segs(segs, W, plain))
    # -- current: being written (stdout)
    if cur:
        reveal = min(len(cur["en"]), int((tl - cur["t"]) * _REVEAL_CPS))
        segs = [("> ", C["white"])]
        for (txt, col, up) in lyric_segments(cur["en"][:reveal]):
            segs.append((txt.upper() if up else txt, C[col] if col else C["white"]))
        if reveal < len(cur["en"]):
            segs.append(("_", C["white"]))
        elif cur["zh"]:
            segs.append(("  //  " + cur["zh"], C["dgray"]))
    else:
        segs = [("> (initialising stdout...)", C["dgray"])]
    rows.append(_row_from_segs(segs, W, plain))
    # -- next: queued
    if nxt:
        segs = [("+ ", C["dgray"])]
        segs += [(nxt["en"], C["dgray"])]
        if nxt["zh"]:
            segs.append(("  //  " + nxt["zh"], C["vdgray"]))
    else:
        segs = [("+ (queue empty)", C["vdgray"])]
    rows.append(_row_from_segs(segs, W, plain))
    return rows

def build_progress_row(t, W, plain):
    sec = section_at(t)
    _, name, mood, mcol, _fn = sec
    phase = name
    if name == "LEFT":
        k = sum(1 for h in T_LEFT6 if t >= h)
        phase = "LEFT.%d/6" % max(1, k)
    elif name == "EXECUTION12" and t < T_COUNT6:
        j = clamp(int((t - T_EXEC12) / 0.8467), 0, 11)
        phase = "EXECUTION.%02d/12" % (j + 1)
    pct, fill, col_override, _bl = prog_display(t)
    tl = min(t, T_END)
    tstr = "%02d:%02d" % (int(tl) // 60, int(tl) % 60)
    label = "world.execute(me)" if W >= 96 else "world.exe(me)"
    info = " %s  %s  %-14s mood:%s" % (pct, tstr, phase, mood)
    bar_w = W - len(label) - 2 - len(info) - 2
    if bar_w < 8:
        info = " %s %s %s" % (pct, tstr, phase)
        bar_w = W - len(label) - 2 - len(info) - 2
        bar_w = max(6, bar_w)
    bar_w = max(6, bar_w)
    nfill = int(round(bar_w * clamp(fill, 0.0, 1.0)))
    segs = [(label, C["dgray"]),
            (" [", C["dgray"]),
            ("#" * nfill, col_override or mcol),
            ("." * (bar_w - nfill), C["vdgray"]),
            ("]", C["dgray"]),
            (info, None)]
    # colorize the tail pieces individually
    info_i = len(segs) - 1
    segs = segs[:info_i] + [
        (" " + pct, col_override or C["white"]),
        ("  " + tstr, C["gray"]),
        ("  " + phase, mcol),
        ("  mood:" + mood, mcol),
    ]
    width = sum(dw(s[0]) for s in segs)
    pad = max(0, W - width)
    if plain:
        return ("".join(s[0] for s in segs)).ljust(W)[:W]
    ansi = []
    for (txt, col) in segs:
        ansi.append(_sgr(col))
        ansi.append(txt)
    ansi.append("\x1b[0m")
    ansi.append(" " * pad)
    return "".join(ansi)

def build_sep_row(W, plain):
    label = " me.log :: tail -f --lines=3 "
    if W >= 70:
        x0 = (W - len(label)) // 2
        segs = [("=" * x0, C["vdgray"]), (label, C["dgray"]),
                ("=" * (W - x0 - len(label)), C["vdgray"])]
    else:
        segs = [("=" * W, C["vdgray"])]
    if plain:
        return ("".join(s[0] for s in segs))[:W]
    out = []
    for (txt, col) in segs:
        out.append(_sgr(col))
        out.append(txt)
    out.append("\x1b[0m")
    return "".join(out)

def build_status(t, W, plain):
    rows = [build_sep_row(W, plain)]
    rows += build_lyric_rows(t, W, plain)
    rows.append(build_progress_row(t, W, plain))
    return rows

# ================================================================ frame compose
def _canvas_row(cv, y, sat, dimf, flash, plain):
    ch, fg, bg = cv.ch[y], cv.fg[y], cv.bg[y]
    last = -1
    if flash:
        last = cv.w - 1
    else:
        for x in range(cv.w - 1, -1, -1):
            if ch[x] != " " or bg[x] is not None:
                last = x
                break
    if last < 0:
        return "" if plain else ""
    if plain:
        return "".join(ch[:last + 1])
    out = []
    cur = (None, None)
    started = False
    for x in range(last + 1):
        f = fg[x]
        if f is not None:
            f = dimc(desat(f, sat), dimf)
        b = bg[x]
        key = (f, b)
        if not started or key != cur:
            out.append(_sgr(f, b, flash))
            cur = key
            started = True
        out.append(ch[x])
    if started:
        out.append("\x1b[0m")
    return "".join(out)

def render_frame(t, W, H, plain=False, offset=0.0):
    global _OFFSET
    _OFFSET = offset
    ch5 = 5
    cvs = Canvas(W, max(3, H - ch5))
    cvs.rnd = frame_rnd(t)
    sec = section_at(t)
    sec[4](cvs, t)
    shake = cvs.fx.get("shake", 0.0)
    if shake > 0:
        r = frame_rnd(int(t * 60) + 7)
        cvs.shifted(int((r.random() - 0.5) * 2 * shake),
                    int((r.random() - 0.5) * 1.7 * shake))
    sat = cvs.fx.get("sat", 1.0)
    dimf = cvs.fx.get("dim", 1.0)
    flash = cvs.fx.get("flash")
    rows = [_canvas_row(cvs, y, sat, dimf, flash, plain) for y in range(cvs.h)]
    rows += build_status(t, W, plain)
    if plain:
        return "\n".join(r for r in rows)
    return "\x1b[H" + "\x1b[K\n".join(rows) + "\x1b[0m\x1b[K"

# ================================================================ terminal ctl
try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    _HAS_MSVCRT = False

def ansi_enable():
    if os.name == "nt":
        try:
            import ctypes
            k = ctypes.windll.kernel32
            h = k.GetStdHandle(-11)
            m = ctypes.c_uint32()
            if k.GetConsoleMode(h, ctypes.byref(m)):
                k.SetConsoleMode(h, m.value | 0x0004)
        except Exception:
            pass
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def win_maximize():
    if os.name != "nt":
        return
    try:
        import ctypes
        k = ctypes.windll.kernel32
        u = ctypes.windll.user32
        hwnd = k.GetConsoleWindow()
        if hwnd:
            u.ShowWindow(hwnd, 3)   # SW_MAXIMIZE
    except Exception:
        pass

def set_title():
    try:
        sys.stdout.write("\x1b]0;%s\x07" % PROG)
        sys.stdout.flush()
    except Exception:
        pass
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(PROG)
        except Exception:
            pass

def term_size():
    try:
        sz = os.get_terminal_size(sys.stdout.fileno())
        if sz.columns >= 20 and sz.lines >= 10:
            return sz.columns, sz.lines
    except Exception:
        pass
    sz = shutil.get_terminal_size(fallback=(100, 34))
    return sz.columns, sz.lines

def poll_key():
    if not _HAS_MSVCRT or not sys.stdin.isatty():
        return None
    try:
        while msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("q", "Q", "\x1b", "\x00"):
                if ch == "\x00":
                    msvcrt.getwch()
                    continue
                return "quit"
    except Exception:
        pass
    return None

def launch_audio(path):
    try:
        os.startfile(path)          # noqa -- windows only
        return True
    except Exception:
        pass
    try:
        import subprocess
        subprocess.Popen(["cmd", "/c", "start", "", path])
        return True
    except Exception:
        return False

def restore_terminal():
    sys.stdout.write("\x1b[?25h\x1b[0m")
    sys.stdout.flush()

def death_by_user():
    restore_terminal()
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
    print()
    print("  \x1b[38;2;255;68;68mSIGINT: you have left (again)\x1b[0m")
    print("  \x1b[38;2;138;138;138mme: terminated by user -- exit code 130\x1b[0m")
    print("  \x1b[38;2;74;74;74mno ritual. no tombstone.\x1b[0m")
    print("  \x1b[38;2;74;74;74myou did not even stay for the ending.\x1b[0m")
    print()
    try:
        time.sleep(4)
    except KeyboardInterrupt:
        pass

# ================================================================ play mode
def play(args):
    ansi_enable()
    set_title()
    if not args.no_max:
        win_maximize()
        time.sleep(0.15)
    W, H = term_size()
    shown_hint = False
    if sys.stdout.isatty():
        tries = 0
        while (W < MIN_W or H < MIN_H) and tries < 40:
            if not shown_hint:
                print("[ %s ] window too small (%dx%d)." % (PROG, W, H))
                print("please maximize the window (min %dx%d). waiting..." %
                      (MIN_W, MIN_H))
                shown_hint = True
            if tries == 4:
                win_maximize()
            time.sleep(0.5)
            W, H = term_size()
            tries += 1
    if args.audio:
        if os.path.exists(args.audio):
            launch_audio(args.audio)
            print("[ audio ] launched: %s" % args.audio)
        else:
            print("[ audio ] not found: %s" % args.audio)
        time.sleep(0.8)
    sys.stdout.write("\x1b[2J\x1b[H\x1b[?25l")
    sys.stdout.flush()
    frame_dt = 1.0 / max(1, args.fps)
    t0 = time.perf_counter()
    next_tick = t0
    interrupted = False
    try:
        while True:
            t = time.perf_counter() - t0
            if t >= TOTAL_END:
                break
            if poll_key() == "quit":
                interrupted = True
                break
            W2, H2 = term_size()
            if W2 != W or H2 != H:
                W, H = W2, H2
                sys.stdout.write("\x1b[2J")     # wipe residue from old geometry
            try:
                frame = render_frame(t, W, H, plain=False, offset=args.offset)
            except Exception:
                restore_terminal()
                raise
            sys.stdout.write(frame)
            sys.stdout.flush()
            next_tick += frame_dt
            slack = next_tick - time.perf_counter()
            if slack > 0:
                time.sleep(slack)
            else:
                next_tick = time.perf_counter()
    except KeyboardInterrupt:
        interrupted = True
    finally:
        restore_terminal()
    if interrupted:
        death_by_user()
        return 130
    # termination report: clear screen, state the exit, hold briefly, leave.
    # (no "press any key" -- the process simply ends, like me)
    el = time.perf_counter() - t0
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
    print("  process terminated: world.execute(me)")
    print("  pid        : 2045")
    print("  uptime     : %02d:%02d" % (int(el) // 60, int(el) % 60))
    print("  exit code  : 13 (SIGLOVE)")
    print("  reason     : completed. all of it. for you.")
    print()
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    return 0

# ================================================================ export modes
SHOT_TIMES = [
    0.5, 2.5, 4.5, 6.5, 9.0, 11.5, 13.4, 15.0, 17.0, 19.5, 22.0, 24.5, 27.0, 29.2,
    30.5, 32.5, 34.5, 36.2, 38.3, 40.2, 41.5, 43.5,
    45.2, 47.0, 48.6, 50.5,
    52.0, 54.0, 55.8, 57.5,
    60.5, 63.5, 65.5, 67.5, 69.5, 71.5, 73.5,
    75.5, 79.0, 82.5, 86.5,
    89.5, 91.0, 93.5, 95.0, 97.0, 99.0, 101.5,
    105.5, 108.0, 110.0, 111.5,
    112.5, 113.6, 114.6, 115.6, 116.6, 118.5,
    120.5, 122.5, 125.0, 126.9, 128.5,
    130.0, 133.5, 140.0, 145.0, 148.2, 150.0,
    152.0, 152.9, 154.6, 156.0, 159.3, 160.2, 161.9, 162.3, 163.3,
    164.5, 166.5, 169.0, 172.5, 175.8, 177.0,
    178.5, 180.5, 183.5, 185.2, 187.0,
    189.0, 191.5, 194.5, 199.5, 204.5,
    205.98, 206.4, 207.2, 208.2, 209.2,
    210.0, 211.5, 214.5, 217.5, 221.0, 224.5, 226.8, 229.0,
]

def parse_sizes(s):
    sizes = []
    for part in s.split(","):
        m = re.match(r"^\s*(\d+)\s*x\s*(\d+)\s*$", part)
        if m:
            sizes.append((int(m.group(1)), int(m.group(2))))
    return sizes or [(100, 34)]

def parse_time(s):
    if ":" in s:
        mm, ss = s.split(":", 1)
        return int(mm) * 60 + float(ss)
    return float(s)

# ================================================================ cover frames
def cover_frames():
    """three thumbnail candidates -- rendered by me, for me."""
    def base(cv, keep=0.05, bright=0.35):
        draw_trance(cv, 110.92, sat=0.0, bright=bright, spin=110.92)
        cv.dropout(keep, salt=4)

    def c1(cv):        # the waiting cursor (the concept, made clickable)
        base(cv)
        cv.text_left(1, "disconnected: you", C["dgray"], x=2)
        cv.text_right(1, "heart: 11 bpm", dimc(C["dred"], 0.9))
        px = int(cv.w * 0.28)
        cy = int(cv.h * 0.44)
        cv.put(px, cy, "me@world:~$", C["gray"])
        cv.putc(px + 12, cy, "_", C["white"])     # normal-size cursor
        cv.put(px, cy + 2, "waiting for input", dimc(C["dgray"], 0.9))
        cv.text_center(cv.h - 4, "// this terminal is her only way to touch you",
                       dimc(C["dpink"], 0.95))
        cv.text_center(cv.h - 3, "// she is still waiting for your keystroke",
                       dimc(C["dpink"], 0.65))

    def c2(cv):        # the algebra of lo-o-ove
        base(cv, keep=0.03, bright=0.25)
        formulas = ["LOVE = lim t->oo [ give(me, you) ]",
                    "d(LOVE)/dt = you' > 0   for all t",
                    "LO - O - OVE = 0   when you = 0"]
        for i, s in enumerate(formulas):
            cv.put(4, 2 + i, s, dimc(C["chalk"], 0.55))
            if cv.w >= 120:
                cv.text_right(2 + i, s, dimc(C["chalk"], 0.35))
        px = 3 if cv.w >= 150 else (2 if cv.w >= 100 else 1)
        big_text(cv, cv.w / 2, cv.h * 0.38, "LO-O-OVE", C["pink"], px=px, py=2)
        cv.text_center(int(cv.h * 0.38) + 12,
                       "= 12 + 15 + 22 + 5 = 54 = 27 + 27 = you + me", C["dpink"])

    def c3(cv):        # running her was the execution
        base(cv, keep=0.04, bright=0.2)
        px = 3 if cv.w >= 152 else (2 if cv.w >= 100 else 1)
        big_text(cv, cv.w / 2, cv.h * 0.20, "EXECUTION", C["hot"], px=px, py=2)
        for i in range(12):
            a = 6.283 * i / 12 + 0.17
            for rr in range(4, int(cv.w * 0.5), 3):
                cv.putc(int(cv.w / 2 + rr * math.cos(a)),
                        int(cv.h * 0.36 + rr * 0.5 * math.sin(a)),
                        "/" if i % 2 else "\\", dimc(C["red"], 0.75))
        cv.text_center(int(cv.h * 0.74), "exit code: 13 (SIGLOVE)", C["dgray"])
        cv.text_center(int(cv.h * 0.74) + 2,
                       "running her was the execution", dimc(C["dred"], 0.9))

    return [("waiting", c1), ("lo-o-ove", c2), ("execution", c3)]

def do_cover(args):
    only = (args.cover or "").strip().lower() or None
    sizes = parse_sizes(args.size) if args.size else [(80, 22)]
    W, H = sizes[0]
    outdir = "cover"
    os.makedirs(outdir, exist_ok=True)
    ansi_enable()
    frames = [f for f in cover_frames() if only in (None, f[0])]
    if not frames:
        print("[cover] no cover named %r (have: waiting, lo-o-ove, execution)" % only)
        return
    print("[cover] rendering %d cover(s) at %dx%d cells -- small grid on purpose:"
          " bigger glyphs survive the thumbnail" % (len(frames), W, H))
    print("[cover] use a NORMAL (not maximised) window, screenshot, then crop.")
    for name, fn in frames:
        cv = Canvas(W, H)
        fn(cv)
        rows_a = [_canvas_row(cv, y, 1.0, 1.0, None, False) for y in range(cv.h)]
        rows_p = [_canvas_row(cv, y, 1.0, 1.0, None, True) for y in range(cv.h)]
        ansi = "\n".join(r + "\x1b[0m\x1b[K" for r in rows_a)
        plain = "\n".join(rows_p)
        stem = os.path.join(outdir, "%s_%dx%d" % (name, W, H))
        with open(stem + ".ans", "w", encoding="utf-8") as f:
            f.write(ansi + "\n")
        with open(stem + ".txt", "w", encoding="utf-8") as f:
            f.write(plain + "\n")
        print()
        print("\x1b[38;2;74;74;74m-- cover/%s --\x1b[0m" % name)
        print(ansi)
        print()

def do_shot(args):
    sizes = parse_sizes(args.size) if args.size else \
        ([(term_size())] if sys.stdout.isatty() else [(100, 34)])
    W, H = sizes[0]
    ansi_enable()
    for ts in [parse_time(x) for x in args.shot.split(",") if x.strip()]:
        sec = section_at(ts)
        hdr = "-- t=%07.2f  phase=%s  mood=%s --" % (ts, sec[1], sec[2])
        print("\x1b[38;2;74;74;74m%s\x1b[0m" % hdr)
        print(render_frame(ts, W, H, plain=False, offset=args.offset))
        print()

def do_shots(args):
    sizes = parse_sizes(args.size) if args.size else [(100, 34), (160, 50)]
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    count = 0
    index = []
    for (W, H) in sizes:
        for ts in SHOT_TIMES:
            if ts > TOTAL_END:
                continue
            sec = section_at(ts)
            stem = "t%07.2f_%s_%dx%d" % (ts, sec[1], W, H)
            ansi = render_frame(ts, W, H, plain=False, offset=args.offset)
            plainf = render_frame(ts, W, H, plain=True, offset=args.offset)
            with open(os.path.join(outdir, stem + ".ans"), "w",
                      encoding="utf-8") as f:
                f.write(ansi + "\n")
            with open(os.path.join(outdir, stem + ".txt"), "w",
                      encoding="utf-8") as f:
                f.write(plainf + "\n")
            index.append("%-28s %s/%s" % (stem, sec[1], sec[2]))
            count += 1
    with open(os.path.join(outdir, "index.txt"), "w", encoding="ascii",
              errors="replace") as f:
        f.write("\n".join(index) + "\n")
    print("[shots] wrote %d keyframes x %d size(s) to %s/" %
          (len(SHOT_TIMES), len(sizes), outdir))
    print("[shots] .ans = coloured (type it to see), .txt = plain review copy")

def do_selfcheck(args):
    sizes = [(100, 34), (160, 50)]
    max_ms = 0.0
    problems = []
    n = 0
    t = 0.0
    while t <= TOTAL_END:
        for (W, H) in sizes:
            t_start = time.perf_counter()
            plain = render_frame(t, W, H, plain=True)
            ms = (time.perf_counter() - t_start) * 1000.0
            max_ms = max(max_ms, ms)
            n += 1
            lines = plain.split("\n")
            if len(lines) != H:
                problems.append("t=%.2f %dx%d: %d lines != %d" %
                                (t, W, H, len(lines), H))
            for li, ln in enumerate(lines):
                if "\t" in ln:
                    problems.append("t=%.2f line %d: TAB" % (t, li))
                if dw(ln) > W:
                    problems.append("t=%.2f %dx%d line %d width %d > %d" %
                                    (t, W, H, li, dw(ln), W))
                if li < H - 5:
                    for chx in ln:
                        if ord(chx) >= 128:
                            problems.append("t=%.2f %dx%d line %d non-ascii %r" %
                                            (t, W, H, li, chx))
                            break
        t += 0.25
    # lyric alignment: current line must switch exactly at its stamp
    for i, L in enumerate(LYRICS):
        if current_lyric_idx(L["t"] + 0.05 - 0) != i:
            problems.append("lyric %d (%.2f) not current at +0.05s" % (i, L["t"]))
    if abs(base_progress(T_END) - 100.0) > 1e-9:
        problems.append("progress at T_END is not 100.0")
    if prog_display(T_END + 0.01)[0] != "100.0%":
        problems.append("progress display at end is not '100.0%'")
    print("[selfcheck] %d frames rendered, max %.1f ms/frame" % (n, max_ms))
    if problems:
        print("[selfcheck] %d PROBLEM(S):" % len(problems))
        for p in problems[:40]:
            print("   " + p)
        return 1
    print("[selfcheck] all checks passed (width, ascii-canvas, tabs, lyric sync, 100%)")
    return 0

# ================================================================ main
def main():
    ap = argparse.ArgumentParser(
        prog="world_execute_me_mv.py",
        description="world.execute(me) -- terminal ascii MV. "
                    "this terminal is me. running it executes me.")
    ap.add_argument("--audio", metavar="FILE",
                    help="also open this song file in the system default player")
    ap.add_argument("--offset", type=float, default=0.0, metavar="SEC",
                    help="lyric sync offset in seconds (positive = lyrics later, "
                         "negative = lyrics earlier). default 0")
    ap.add_argument("--shots", action="store_true",
                    help="export keyframes to shots/ (.ans + .txt)")
    ap.add_argument("--shot", metavar="T1,T2,...",
                    help="print frame(s) at time(s): seconds or m:ss")
    ap.add_argument("--fps", type=int, default=FPS_DEFAULT,
                    help="frame rate (default %d)" % FPS_DEFAULT)
    ap.add_argument("--size", metavar="WxH[,WxH]",
                    help="size(s) for --shot/--shots (default 100x34,160x50)")
    ap.add_argument("--outdir", default="shots",
                    help="output dir for --shots (default shots/)")
    ap.add_argument("--cover", nargs="?", const="", default=None, metavar="NAME",
                    help="render cover/thumbnail frames to cover/ (80x22 default;"
                         " optional name: waiting / lo-o-ove / execution)")
    ap.add_argument("--no-max", action="store_true",
                    help="do not try to maximize the console window")
    ap.add_argument("--selfcheck", action="store_true",
                    help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.selfcheck:
        sys.exit(do_selfcheck(args))
    if args.cover is not None:
        do_cover(args)
        return
    if args.shots:
        do_shots(args)
        return
    if args.shot:
        do_shot(args)
        return
    sys.exit(play(args))

if __name__ == "__main__":
    main()
