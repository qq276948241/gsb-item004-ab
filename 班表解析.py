# -*- coding: utf-8 -*-

from 名字规则 import 名字行不行
from 时间换算 import 读出分钟, 凑结束点


def 解析行们(行们):
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
    return 问题, 有效
