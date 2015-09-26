#-*- coding: utf-8 -*-
__author__ = 'hyeongminpark'
import csv

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
        row = [int(row[0]), row[1].strip().decode('UTF-8')]
        point_table.append(row[0:2])


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