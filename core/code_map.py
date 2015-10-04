#-*- coding: utf-8 -*-
__author__ = 'hyeongminpark'
import csv

POINT_CODE = 0
NAME = 1
TAG_LIST = 2


point_table = []
# with open("point_code.csv", newline='') as csvfile:
#     data_reader = csv.reader(csvfile)
#     for row in data_reader:
#         # row[0] = int(row[0])
#         # row[1] = row[1].strip()
#         row = [int(row[0]), row[1].strip()]
#         point_table.append(row[0:2])

with open('point_code.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        new_row = [int(row[0]), row[1].strip().decode('UTF-8')]

        raw_tag_list = [row[2], row[3], row[4], row[5]]
        # print(raw_tag_list)
        tag_list = []
        for tag in raw_tag_list:
            if tag is not '':
                tag_list.append(int(tag))

        new_row.append(tag_list)
        point_table.append(new_row)


def pointCode2tagList(pointCode):
    for point in point_table:
        if point[POINT_CODE] == pointCode:
            # print "found the point: " + str(pointCode) + code2point(pointCode)
            # print "point[TAG_LIST]" + str(point[TAG_LIST])
            return point[TAG_LIST]
    return []


weight_table = [
    [1, "lodging"],
    [2, "shopping"],
    [3, "food"],
    [4, "transport"],
    [5, "entertainment"],
    [6, "culture"],
    [7, "landscape"],
    [8, "street"],
    [9, "security"],
    [10, "kpop"],
    [11, "medical"],
    [12, "beauty"]
]


def weight_table_code2meaning(code):
    for item in weight_table:
        if item[0] == code:
            return item[1]


def weight_table_meaning2code(meaning):
    for item in weight_table:
        if item[1] == meaning:
            return item[0]


city_table = [
    [1, "서울"],
    [2, "부산"],
    [3, "대구"],
    [4, "인천"],
    [5, "광주"],
    [6, "울산"],
    [7, "대전"],
    [8, "경기"],
    [9, "강원"],
    [10, "충북"],
    [11, "충남"],
    [12, "전북"],
    [13, "전남"],
    [14, "경북"],
    [15, "경남"],
    [16, "제주"],
    [17, "세종"],
    [97, "기타"],
    [99, "없다/모름/무응답"]
]


area_table = [
    [1, "서울"],
    [2, "인천"],
    [3, "경기"],
    [4, "강원"],
    [5, "충청"],
    [6, "경상"],
    [7, "전라"],
    [8, "제주"],
    [9, "기타"],
    [99, "없다/모름/무응답"]
]


def code2point(code):
    for row in point_table:
        if row[0] == code:
            return row[1]


def code2city(code):
    for row in city_table:
        if row[0] == code:
            return row[1]


def code2area(code):
    for row in area_table:
        if row[0] == code:
            return row[1]