# -*- coding: utf-8 -*-

最少歇息 = 11 * 60


def 读出分钟(文本):
    if not isinstance(文本, str):
        return None
    片段 = 文本.split(":")
    if len(片段) != 2:
        return None
    if len(片段[0]) != 2 or len(片段[1]) != 2:
        return None
    if (not 片段[0].isdigit()) or (not 片段[1].isdigit()):
        return None
    时 = int(片段[0])
    分 = int(片段[1])
    if 时 < 0 or 时 > 23 or 分 < 0 or 分 > 59:
        return None
    return 时 * 60 + 分


def 凑结束点(标记, 开始, 结束):
    if 标记 == "跨夜":
        return 结束 + 24 * 60
    return 结束


def 白班要不要挪到下一天(某人的班, 这一段):
    有跨夜 = False
    巡 = 0
    while 巡 < len(某人的班):
        if 某人的班[巡]["标记"] == "跨夜":
            有跨夜 = True
            break
        巡 = 巡 + 1
    if not 有跨夜:
        return False
    if 这一段["标记"] != "白班":
        return False
    正午 = 12 * 60
    if 这一段["开始"] < 正午:
        return True
    return False
