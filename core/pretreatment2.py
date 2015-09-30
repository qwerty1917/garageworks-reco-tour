#-*- coding: utf-8 -*-
__author__ = 'hyeongminpark'
import csv
import time
from random import shuffle
from operator import itemgetter

### 상수
EXPENSE_OF_ALL_PER_MAN_MEAN = 1436.4
DATA_TRUNCATE = 2000

def create_raw_table_from_csv(dir):

    raw_data_table=[]
    # with open(dir, newline='') as csvfile:
    #     data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for count, row in enumerate(data_reader):
    #         raw_data_table.append(row)

    with open(dir, 'rb') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in data_reader:
            raw_data_table.append(row)
            # row = [int(row[0]), row[1].strip().decode('UTF-8')]
            # point_table.append(row[0:2])

    raw_table=[]
    for i in range(len(raw_data_table)):
        row = raw_data_table[i][0].split(",")
        del row[1]

        if i == 0:
            row[0] = 'id'

        raw_table.append(row)

    column_index = raw_table[0]
    del raw_table[0]

    new_raw_table = []
    for line in raw_table:
        new_line = []
        for item in line:
            if item == '':
                new_line.append(0)
                continue
            try:
                new_line.append(float(item))
            except ValueError:
                new_line.append(item)
        new_raw_table.append(new_line)

    raw_table = new_raw_table
    return column_index, raw_table

### 데이터 처리는 raw_table 과 column_index 로 수행한다.


def column_none_ratio(col_name, column_index, raw_table):
    total_count = len(raw_table)
    none_count=0
    for i in range(total_count):
        if raw_table[i][column_index.index(col_name)] == None:
            none_count = none_count+1
    result = none_count/total_count

    print("\n===== column_none_ratio ======")
    print("** col name: %s"%col_name)
    print("** none ratio: %f%%"%result)
    print("============= end =============\n")

    return result


def column_distribution_check(col_name, column_index, raw_table):
    total_count = len(raw_table)
    data_list = []
    for i in range(total_count):
        data_list.append(raw_table[i][column_index.index(col_name)])

    data_set = sorted(list(set(data_list)), key=lambda x: (x is not None, x))
    discrete_data_count = len(data_set)
    print("\n===== column_distribution_check ======")
    print("** col name: %s"%col_name)
    print("** data set: %s"%str(data_set))
    print("** discrete data: %d"%discrete_data_count)
    print("** data distribution: ")
    for item in data_set:
        print("    %s : %0.2f%%, %d times"%(str(item), item_in_list_ratio_in_percent(item, data_list), data_list.count(item)))
    print("================ end =================\n")

    return (discrete_data_count, data_set)

def item_in_list_ratio_in_percent(item, list):
    return 100*list.count(item)/len(list)

def create_col_check_list_x():
    col_check_list_x = ["motive_of_tour_1",
                        "motive_of_tour_2",
                        "motive_of_tour_3",
                        "accompany_with_alone",
                        "accompany_with_family",
                        "accompany_with_friend",
                        "accompany_with_colleague",
                        "accompany_with_etc",
                        "num_accompany_origin",
                        "stay_period_origin",
                        "expense_of_all_per_man",
                        "total_expense_of_lodging_per_man",
                        "total_expense_of_shopping",
                        "total_expense_of_food",
                        "total_expense_of_transport",
                        "total_expense_of_entertainment",
                        "total_expense_of_culture"]

    tour_visit_points = ["tour_visit_point_"+str(i) for i in range(1, 34)]
    tour_visit_cities = ["tour_visit_city_"+str(i) for i in range(1, 100)]
    tour_visit_areas = ["tour_visit_area_"+str(i) for i in range(1, 100)]

    return col_check_list_x, tour_visit_points, tour_visit_cities, tour_visit_areas


def col_truncate(col_index_to_leave, prev_column_index, raw_table):
    # print("raw_table len: " + str(len(raw_table)))
    new_column_index = []
    new_table = []

    for cherry_col in col_index_to_leave:
        if cherry_col in prev_column_index:
            new_column_index.append(cherry_col)

    for row in raw_table:
        new_row = []
        for cherry_col in new_column_index:
            new_row.append(row[prev_column_index.index(cherry_col)])
        new_table.append(new_row)

    return new_column_index, new_table


def row_truncate_by_satisfaction(column_index, raw_table):
    key_column_index = "satisfaction_overall"
    value_list_to_leave = [4.0, 5.0]
    ## 1:매우불만 2:불만 3:보통 4:만족 5:매우만족

    new_table = []
    for data_point in raw_table:
        if data_point[column_index.index(key_column_index)] in value_list_to_leave:
            new_table.append(data_point)

    return column_index, new_table


def make_input(motive_of_tour_1,        # nominal
               motive_of_tour_2,        # nominal
               motive_of_tour_3,        # nominal

               accompany_kind,          # nominal

               accompany_num,           # ratio
               stay_period,             # ratio
               expense_of_all_per_man,  # ratio

                                        ## 가중치는 5단계(0,1,2,3,4,5) <- 가중치 0이 제외된 항목임.
               weight_lodging,          # ordinal
               weight_shopping,         # ordinal
               weight_food,             # ordinal
               weight_transport,        # ordinal
               weight_entertainment,    # ordinal
               weight_culture           # ordinal
               ):
    """
    input parameter:

        motive_of_tour_1
        motive_of_tour_2
        motive_of_tour_3
            range of motive_of_tour_1~3 : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 97]

        accompany_kind
            range of accompany_kind : [1, 2, 3, 4, 5]

        accompany_num
            range of accompany_num : int

        stay_period
            range of stay_period : int

        expense_of_all_per_man
            range of expense_of_all_per_man : int

        weight_lodging
        weight_shopping
        weight_food
        weight_transport
        weight_entertainment
        weight_culture
            range of weight_lodging~culture : [0, 1, 2, 3, 4, 5]


    index of output dict:

        motive_of_tour_1
        motive_of_tour_2
        motive_of_tour_3
        accompany_with_alone
        accompany_with_family
        accompany_with_friend
        accompany_with_colleague
        accompany_with_etc
        num_accompany_origin
        stay_period_origin
        expense_of_all_per_man
        weight_lodging
        weight_shopping
        weight_food
        weight_transport
        weight_entertainment
        weight_culture
    """

    #### parameter 검사

    motivation_code_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 97]
    accompany_kind_code_list = [1, 2, 3, 4, 5]
    weight_code_list = [0, 1, 2, 3, 4, 5]
    if (motive_of_tour_1 not in motivation_code_list) or \
            (motive_of_tour_2 not in motivation_code_list) or \
            (motive_of_tour_3 not in motivation_code_list):
        raise ValueError("motive_of_tour should be in %s" % str(motivation_code_list))

    elif accompany_kind not in accompany_kind_code_list:
        raise ValueError("accompany_kind should be in %s" % str(accompany_kind_code_list))

    elif type(accompany_num).__name__ != 'int':
        raise TypeError("accompany_num should be int. %s detected." % type(accompany_num).__name__)

    elif type(stay_period).__name__ != 'int':
        raise TypeError("stay_period should be int. %s detected." % type(stay_period).__name__)

    elif type(expense_of_all_per_man).__name__ != 'int':
        raise TypeError("expense_of_all_per_man should be int. %s detected." % type(expense_of_all_per_man).__name__)

    elif (weight_lodging not in weight_code_list) or \
            (weight_shopping not in weight_code_list) or \
            (weight_food not in weight_code_list) or \
            (weight_transport not in weight_code_list) or \
            (weight_entertainment not in weight_code_list) or \
            (weight_culture not in weight_code_list):
        raise ValueError("weight value should be in %s" % str(weight_code_list))

    else:
        pass

    #### parameter 검사 끝


    input_dict = {}

    input_dict["motive_of_tour_1"] = motive_of_tour_1
    input_dict["motive_of_tour_2"] = motive_of_tour_2
    input_dict["motive_of_tour_3"] = motive_of_tour_3

    input_dict["accompany_with_alone"] \
    = input_dict["accompany_with_family"] \
    = input_dict["accompany_with_friend"] \
    = input_dict["accompany_with_colleague"] \
    = input_dict["accompany_with_etc"] = None

    if accompany_kind == 1:
        input_dict["accompany_with_alone"] = 1.0
    elif accompany_kind == 2:
        input_dict["accompany_with_family"] = 2.0
    elif accompany_kind == 3:
        input_dict["accompany_with_friend"] = 3.0
    elif accompany_kind == 4:
        input_dict["accompany_with_colleague"] = 4.0
    elif accompany_kind == 5:
        input_dict["accompany_with_etc"] = 5.0
    else:
        pass

    input_dict["num_accompany_origin"] = 1
    if accompany_num != None:
        input_dict["num_accompany_origin"] = accompany_num

    input_dict["stay_period_origin"] = stay_period
    input_dict["expense_of_all_per_man"] = expense_of_all_per_man

    input_dict["weight_lodging"] = weight_lodging
    input_dict["weight_shopping"] = weight_shopping
    input_dict["weight_food"] = weight_food
    input_dict["weight_transport"] = weight_transport
    input_dict["weight_entertainment"] = weight_entertainment
    input_dict["weight_culture"] = weight_culture

    return input_dict


def rankList(list):
    resultList = []
    rankDict = {}
    listSet = set(list)
    for i in listSet:
        rankDict[i] = list.count(i)

    # print(rankDict)

    while len(rankDict) != 0:
        maxKey = max(rankDict.iteritems(), key=itemgetter(1))[0]
        resultList.append(maxKey)
        rankDict.pop(maxKey, None)

    return resultList


def diviner(input_dict,             # input x dict

            total_col_index,         # x total index

            data_table,             # data table

            tour_visit_points,      # y detail index
            tour_visit_cities,
            tour_visit_areas,):

    # print("total_col_index len: " + str(len(total_col_index)) + ", data_table col num: " + str(len(data_table[0])))

    nominal_x_list = ["motive_of_tour_1",
                      "motive_of_tour_2",
                      "motive_of_tour_3",
                      "accompany_with_alone",
                      "accompany_with_family",
                      "accompany_with_friend",
                      "accompany_with_colleague",
                      "accompany_with_etc"]

    ratio_x_list = ["num_accompany_origin",
                    "stay_period_origin",
                    "expense_of_all_per_man"]

    ordinal_weight_list = ["weight_lodging",
                           "weight_shopping",
                           "weight_food",
                           "weight_transport",
                           "weight_entertainment",
                           "weight_culture"]

    expenses_by_field = ["total_expense_of_lodging_per_man",
                         "total_expense_of_shopping",
                         "total_expense_of_food",
                         "total_expense_of_transport",
                         "total_expense_of_entertainment",
                         "total_expense_of_culture"]

    # ratio 컬럼들 정규화
    print("start normalization")
    normalization_start_time = time.time()
    for ratio_col in ratio_x_list:
        # print(ratio_col)
        single_col_data_list = []
        for row in data_table:
            single_col_data_list.append(row[total_col_index.index(ratio_col)])
        # print("single_col_data_list len: " + str(len(single_col_data_list)))

        input_dict[ratio_col] = normalization(input_dict[ratio_col], single_col_data_list)
        for i in range(len(data_table)):
            data_table[i][total_col_index.index(ratio_col)] = normalization(data_table[i][total_col_index.index(ratio_col)], single_col_data_list)
    normalization_end_time = time.time()
    print("end normalization")
    print("time on normalization: " + str(normalization_end_time - normalization_start_time) + "\n =====================")


    print("starting kNN")
    kNN_start_time = time.time()
    # ratio 기준으로 가장 가까운 포인트 50개 구한다.
    best50_table = []
    dists_in_best50 = []
    total_d = d_len = 0 #test code
    for row in data_table:
        dsq = 0
        # print("==== "+ratio_col+" ====")
        """ ratio vars
        num_accompany_origin
        stay_period_origin
        expense_of_all_per_man
        """
        for ratio_col in ratio_x_list:
            if row[total_col_index.index(ratio_col)] != None and input_dict[ratio_col] != None:
                tmp_dsq = (row[total_col_index.index(ratio_col)] - input_dict[ratio_col])**2
                dsq = dsq + tmp_dsq
            else:
                dsq = 100
                continue
                # print("dist for "+ratio_col +" : "+str(tmp_dsq**(1/2)))
        # print("========")

        d = dsq**(1/2)
        if len(best50_table) < 50:
            best50_table.append(row)
            dists_in_best50.append(d)

        elif d < max(dists_in_best50):
            index_to_del = dists_in_best50.index(max(dists_in_best50))
            del best50_table[index_to_del]
            del dists_in_best50[index_to_del]

            best50_table.append(row)
            dists_in_best50.append(d)

        total_d = total_d + d #test code
        d_len = d_len + 1
    # print("d mean : " + str(total_d/d_len))
    # print("best d list: " + str(dists_in_best50))
    kNN_end_time = time.time()
    print("ending kNN")
    print("time on kNN: " + str(kNN_end_time - kNN_start_time) + "\n =====================")


    # 위의 50개 포인트 중 nominal, ordinal 를 기준으로 순위를 정한다. table: best50_table, index: total_col_index
    print("starting nominal / ordinal ranking")
    rank_start_time = time.time()

    rank_table = [] # rank_table[0] : rank, rank_table[1] : data row
    for row in best50_table:
        grade = 0
        """ nominal vars
        motive_of_tour_1
        motive_of_tour_2
        motive_of_tour_3
        accompany_with_alone
        accompany_with_family
        accompany_with_friend
        accompany_with_colleague
        accompany_with_etc
        """
        for norminal_col in nominal_x_list:
            if row[total_col_index.index(norminal_col)] == input_dict[norminal_col]:
                if norminal_col == "motive_of_tour_1":
                    grade += 3
                elif norminal_col == "motive_of_tour_2":
                    grade += 2
                elif norminal_col == "motive_of_tour_3":
                    grade += 1
                else:
                    grade += 3

        """ ordinal input vars (ordinal_weight_list)
        weight_lodging
        weight_shopping
        weight_food
        weight_transport
        weight_entertainment
        weight_culture
        """
        """ ordinal data vars (row[total_col_index.index(<col_name>)] <col_name> in expenses_by_field)
        total_expense_of_lodging_per_man
        total_expense_of_shopping
        total_expense_of_food
        total_expense_of_transport
        total_expense_of_entertainment
        total_expense_of_culture
        """
        # print("====\n====")
        data_weight_list = []
        for index, expense_by_field in enumerate(expenses_by_field):
            data_weight_list.append([index, row[total_col_index.index(expense_by_field)]])
            # print(ordinal_weight_list[index], row[total_col_index.index(expense_by_field)])
        data_weight_list = sorted(data_weight_list, key=itemgetter(1), reverse=True)
        data_weight_sequence = []
        for data_weight_row in data_weight_list:
            data_weight_sequence.append(data_weight_row[0])
        # for i in data_weight_sequence:
        #     print(i)
        # print("===")
        input_weight_list = []
        for index, weight_by_field in enumerate(ordinal_weight_list):
            input_weight_list.append([index, input_dict[weight_by_field]])
        input_weight_list = sorted(input_weight_list, key=itemgetter(1), reverse=True)
        input_weight_sequence = []
        for input_weight_row in input_weight_list:
            input_weight_sequence.append(input_weight_row[0])

        # for i in input_weight_sequence:
        #     print (i)

        list_diff = 0
        for index in range(len(input_weight_sequence)):
            num_diff = abs(input_weight_sequence[index]-data_weight_sequence[index])
            list_diff += num_diff
        list_similarity = 9 - list_diff
        # print("list_similarity", list_similarity)

        grade += list_similarity

        rank_table.append([grade, row])

    rank_table = sorted(rank_table, key=itemgetter(0), reverse=True)


    result_data_table = []
    for i in range(20):
        result_data_table.append(rank_table[i][1])

    points_final_list = [] # 한국여행 방문지
    cities_final_list = [] # 한국여행 방문지 시도별
    areas_final_list  = [] # 한국여행 방문지 권역별
    for row in result_data_table:
        for i, index in enumerate(total_col_index):
            if "tour_visit_point_" in index:
                points_final_list.append(row[i])
            elif "tour_visit_city_" in index:
                cities_final_list.append(row[i])
            elif "tour_visit_area_" in index:
                areas_final_list.append(row[i])
    points_final_list = [int(i) for i in points_final_list]
    cities_final_list = [int(i) for i in cities_final_list]
    areas_final_list = [int(i) for i in areas_final_list]

    point_reco = rankList(points_final_list)
    city_reco = rankList(cities_final_list)
    area_reco = rankList(areas_final_list)


    # print(point_reco[2:32])
    # print(city_reco[2:])
    # print(area_reco[2:])



    # for index, item in enumerate(best50_table[10]):
    #     print(total_col_index[index], item)




    rank_end_time = time.time()
    print("ending nominal / ordinal ranking")
    print("time on nominal / ordinal ranking: " +str(rank_end_time - rank_start_time) + "\n =====================")


    # 위로부터 적당히 잘라서 목적지 반환

    return {"point_reco":point_reco[3:32], "city_reco":city_reco[3:], "area_reco":area_reco[3:], "most_visit":point_reco[:3]}


def normalization(x, raw_list):
    if None in raw_list:
        new_list = raw_list.remove(None)
    else:
        new_list = raw_list
    return (x - min(new_list))/(max(new_list) - min(new_list))


def denormalization(z, raw_list):
    if None in raw_list:
        new_raw_list = raw_list.remove(None)
    else:
        new_raw_list = raw_list
    return z*(max(new_raw_list) - min(new_raw_list)) + min(new_raw_list)


def reco_wizard(motive_of_tour_1,        # nominal
                motive_of_tour_2,        # nominal
                motive_of_tour_3,        # nominal

                accompany_kind,          # nominal

                accompany_num,           # ratio
                stay_period,             # ratio
                expense_of_all_per_man,  # ratio

                                        ## 가중치는 5단계(0,1,2,3,4,5) <- 가중치 0이 제외된 항목임.
                weight_lodging,          # ordinal
                weight_shopping,         # ordinal
                weight_food,             # ordinal
                weight_transport,        # ordinal
                weight_entertainment,    # ordinal
                weight_culture           # ordinal
                ):
    total_time_start = time.time()
    column_index, raw_table = create_raw_table_from_csv('eng_code_mapped_csv.csv')

    ### 데이터 너무 커서 임시로 자름!
    shuffle(raw_table)
    raw_table=raw_table[:DATA_TRUNCATE]
    ### 이까지

    # print("raw data len: " + str(len(raw_table)))
    column_index, positive_table = row_truncate_by_satisfaction(column_index, raw_table)
    # print("positive data col num: "+ str(len(positive_table[0])) + ", index len : " + str(len(column_index)))
    # print("positive datapoint: " + str(len(positive_table)))

    col_check_list_x, tour_visit_points, tour_visit_cities, tour_visit_areas = create_col_check_list_x()

    new_col_ind = col_check_list_x + tour_visit_points + tour_visit_cities + tour_visit_areas
    # print("new_col_ind len: "+ str(len(new_col_ind)) + ", set len: " + str(len(set(new_col_ind)))) # 지역, 도시 코드가 1~100 모두 다 있는것은 아니라 좀 더 많아짐

    trc_col_ind, trc_tbl = col_truncate(new_col_ind, column_index, positive_table)
    # print(len(trc_col_ind), len(trc_tbl[0]))

    result_dict = diviner(make_input(motive_of_tour_1,
                       motive_of_tour_2,
                       motive_of_tour_3,
                       accompany_kind,
                       accompany_num,
                       stay_period,
                       expense_of_all_per_man,
                       weight_lodging,
                       weight_shopping,
                       weight_food,
                       weight_transport,
                       weight_entertainment,
                       weight_culture), trc_col_ind, trc_tbl, tour_visit_points, tour_visit_cities, tour_visit_areas)


    ### test code

    # print("%d X %d mat"%(len(trc_tbl), len(trc_tbl[0])))



    # column_distribution_check("motive_of_tour_2", column_index, raw_table)

    # print(trc_col_ind[2])
    # for i in range(100):
    #     print(str(trc_tbl[i][trc_col_ind.index(trc_col_ind[0])]) + " " + str(raw_table[i][column_index.index(trc_col_ind[0])]))

    # print(len(trc_tbl[0]))
    # for x in col_check_list_x:
    #     column_none_ratio(x, column_index, raw_table)
    #     column_distribution_check(x, column_index, raw_table)
    total_time_end = time.time()
    print("total time: " + str(total_time_end-total_time_start))

    return result_dict