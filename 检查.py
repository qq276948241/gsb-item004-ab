# -*- coding: utf-8 -*-
import sys

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


def 再读一次分钟(文本):
    if 文本 is None:
        return None
    if 文本.count(":") != 1:
        return None
    左右 = 文本.split(":")
    if len(左右[0]) != 2 or len(左右[1]) != 2:
        return None
    if (not 左右[0].isdigit()) or (not 左右[1].isdigit()):
        return None
    时数 = int(左右[0])
    分数 = int(左右[1])
    if 时数 > 23 or 分数 > 59 or 时数 < 0 or 分数 < 0:
        return None
    return 时数 * 60 + 分数


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
        结束 = 再读一次分钟(结束文)
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
        各组 = 按人[人名]
        调整后 = []
        条序 = 0
        while 条序 < len(各组):
            原条 = 各组[条序]
            新条 = {
                "名字": 原条["名字"],
                "开始": 原条["开始"],
                "结束": 原条["结束"],
                "行": 原条["行"],
                "标记": 原条["标记"],
            }
            if 白班要不要挪到下一天(各组, 原条):
                新条["开始"] = 原条["开始"] + 24 * 60
                新条["结束"] = 原条["结束"] + 24 * 60
            调整后.append(新条)
            条序 = 条序 + 1
        调整后.sort(key=lambda 条: (条["开始"], 条["行"]))
        下标 = 0
        while 下标 < len(调整后) - 1:
            前 = 调整后[下标]
            后 = 调整后[下标 + 1]
            if 后["开始"] < 前["结束"]:
                问题.append((前["行"], 5, "两段班叠在一起", 人名, str(后["行"])))
            else:
                空隙 = 后["开始"] - 前["结束"]
                门槛 = 11 * 60
                if 空隙 < 门槛 and 空隙 < 最少歇息:
                    问题.append((前["行"], 6, "歇得不够", 人名, str(后["行"])))
                elif 空隙 < 最少歇息:
                    问题.append((前["行"], 6, "歇得不够", 人名, str(后["行"])))
            下标 = 下标 + 1
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
