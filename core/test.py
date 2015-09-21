#-*- coding: utf-8 -*-
__author__ = 'hyeongminpark'
import pretreatment2
reco_dict = pretreatment2.reco_wizard(4, 5, 6, 2, 5, 14, 25000, 3, 4, 5, 0, 0, 0)

print(reco_dict)
"""
사용방법: eng_code_mapped_csv.csv와 pretreatment2 두 파일을 호출하고자 하는 파이썬 파일(아마도 app controller)과 같은 디렉토리에 두고 위의 3,4번 라인 그대로 호출해서 사용하면 됨.
        reco_wizard 함수의 입출력 상세는 아래 명시함.

input parameter:
    === 총 16개의 입력변수가 요구됨 상세는 아래 ===

    motive_of_tour_1
    motive_of_tour_2
    motive_of_tour_3
        range of motive_of_tour_1~3 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 97] (=== 코드북 q5a1~q5a3 참조 ===)

    accompany_kind
        range of accompany_kind : [1, 2, 3, 4, 5] (1: 혼자, 2: 가족/친지, 3: 친구/연인, 4: 직장동료, 5: 기타)

    accompany_num
        range of accompany_num : int (몇명이서 왔는지)

    stay_period
        range of stay_period : int (몇일이나 있을 것인지)

    expense_of_all_per_man
        range of expense_of_all_per_man : int (얼마나 쓸 것인지 달러기준)

    weight_lodging
    weight_shopping
    weight_food
    weight_transport
    weight_entertainment
    weight_culture
        range of weight_lodging~culture : [0, 1, 2, 3, 4, 5] (0은 선택안함에 해당. 숫자 클수록 중요도 커짐)


key of output dict:
    === 코드북 참조 ===
    "city_reco" : 17개시도별 한국여행 방문지 (길이가 유동적으로 변함. 최대 19개. 보통 5개 내외)
    "area_reco" : 권역별 한국여행 관광지 (길이가 유동적으로 변함. 최대 10개 보통. 5개 내외)
    "point_reco" : 한국여행 관광지 (이론적으로는 최대 30개 추천함. - 하지만 거의 항상 30개라고 보면 됨. 잘 안변함.)
    """