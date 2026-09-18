# -*- coding: utf-8 -*-


def 名字行不行(名字):
    if 名字 is None or 名字 == "":
        return False
    if len(名字) > 4:
        return False
    下标 = 0
    while 下标 < len(名字):
        单字 = 名字[下标]
        if not ("一" <= 单字 <= "鿿"):
            return False
        下标 = 下标 + 1
    return True
