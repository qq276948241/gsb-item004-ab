# -*- coding: utf-8 -*-
import sys

from 时间换算 import 读出分钟, 凑结束点
from 班表规则 import 名字行不行
from 班次分析 import 查一个人


def 跑(路径):
    try:
        文件 = open(路径, "r", encoding="utf-8")
    except OSError:
        sys.stdout.write("时间写不出来｜第0行｜样例\n")
        return 1
    原文 = 文件.read()
    文件.close()
    行们 = 原文.splitlines()
    问题 = []
    有效 = []
    行号 = 0
    for 原始 in 行们:
        行号 = 行号 + 1
        去空白 = 原始.strip()
        if 去空白 == "":
            continue
        if 去空白.startswith("注"):
            continue
        段 = 去空白.split("|")
        if len(段) != 4:
            名字占位 = 段[0].strip() if len(段) > 0 else ""
            if 名字占位 == "":
                名字占位 = "空"
            问题.append((行号, 2, "时间写不出来", 名字占位, ""))
            continue
        名字 = 段[0].strip()
        开始文 = 段[1].strip()
        结束文 = 段[2].strip()
        标记 = 段[3].strip()
        if not 名字行不行(名字):
            if 名字 == "":
                名字 = "空"
            问题.append((行号, 1, "名字不合规", 名字, ""))
            continue
        开始 = 读出分钟(开始文)
        结束 = 读出分钟(结束文)
        if 开始 is None or 结束 is None:
            问题.append((行号, 2, "时间写不出来", 名字, ""))
            continue
        if 标记 != "白班" and 标记 != "跨夜":
            问题.append((行号, 2, "时间写不出来", 名字, ""))
            continue
        if 开始 == 结束:
            问题.append((行号, 3, "起止写反", 名字, ""))
            continue
        if 标记 == "白班" and 结束 < 开始:
            问题.append((行号, 3, "起止写反", 名字, ""))
            continue
        if 标记 == "跨夜" and 结束 >= 开始:
            问题.append((行号, 4, "夜里没标清楚", 名字, ""))
            continue
        结束点 = 凑结束点(标记, 开始, 结束)
        有效.append({
            "名字": 名字,
            "开始": 开始,
            "结束": 结束点,
            "行": 行号,
            "标记": 标记,
        })

    按人 = {}
    序号 = 0
    while 序号 < len(有效):
        条 = 有效[序号]
        if 条["名字"] not in 按人:
            按人[条["名字"]] = []
        按人[条["名字"]].append(条)
        序号 = 序号 + 1

    人名列表 = []
    for 人名 in 按人:
        人名列表.append(人名)
    人名列表.sort()

    人序 = 0
    while 人序 < len(人名列表):
        人名 = 人名列表[人序]
        问题.extend(查一个人(人名, 按人[人名]))
        人序 = 人序 + 1

    问题.sort(key=lambda 项: (项[0], 项[1], 项[4]))
    if len(问题) == 0:
        sys.stdout.write("班表没有问题\n")
        return 0
    写出 = 0
    while 写出 < len(问题):
        项 = 问题[写出]
        if 项[4] != "":
            一行 = "第%s行｜%s｜%s｜对着第%s行\n" % (项[0], 项[2], 项[3], 项[4])
            sys.stdout.write(一行)
        else:
            一行 = "第%s行｜%s｜%s\n" % (项[0], 项[2], 项[3])
            sys.stdout.write(一行)
        写出 = 写出 + 1
    return 1


def 入口():
    路径 = "样例"
    if len(sys.argv) > 1:
        路径 = sys.argv[1]
    状态 = 跑(路径)
    raise SystemExit(状态)


if __name__ == "__main__":
    入口()
