# -*- coding: utf-8 -*-
import sys

from 班表解析 import 解析行们
from 班次比对 import 比对班次


def 跑(路径):
    try:
        文件 = open(路径, "r", encoding="utf-8")
    except OSError:
        sys.stdout.write("时间写不出来｜第0行｜样例\n")
        return 1
    原文 = 文件.read()
    文件.close()
    行们 = 原文.splitlines()
    问题, 有效 = 解析行们(行们)
    问题 = 问题 + 比对班次(有效)

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
