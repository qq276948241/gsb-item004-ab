# -*- coding: utf-8 -*-


def 名字行不行(名字):
    if 名字 is None or 名字 == "":
        return False
    if len(名字) > 4:
        return False
    下标 = 0
    while 下标 < len(名字):
        单字 = 名字[下标]
        if not ("\u4e00" <= 单字 <= "\u9fff"):
            return False
        下标 = 下标 + 1
    return True


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
