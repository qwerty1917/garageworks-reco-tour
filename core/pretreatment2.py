__author__ = 'hyeongminpark'
import csv
raw_data_table=[]
with open('eng_code_mapped_csv.csv', newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for count, row in enumerate(data_reader):
        raw_data_table.append(row)

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
            new_line.append(None)
            continue
        try:
            new_line.append(float(item))
        except ValueError:
            new_line.append(item)
    new_raw_table.append(new_line)

raw_table = new_raw_table

### 데이터 처리는 raw_table 과 column_index 로 수행한다.


def column_none_ratio(col_name):
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

def column_distribution_check(col_name):
    total_count = len(raw_table)
    data_list = []
    for i in range(total_count):
        data_list.append(raw_table[i][column_index.index(col_name)])

    data_set = sorted(list(set(data_list)), key=lambda x: (x is not None, x))
    discrete_data_count = len(data_set)
    print("\n===== column_distribution_check ======")
    print("** col name: %s"%col_name)
    print("** data set: %s"%str(data_set))
    print("** data discrete: %d"%discrete_data_count)
    print("================ end =================\n")

    return (discrete_data_count, data_set)

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

def make_input(motive_of_tour_1,        # nominal
               motive_of_tour_2,        # nominal
               motive_of_tour_3,        # nominal

               accompany_kind,          # nominal

               accompany_num,           # ratio
               stay_period,             # ratio
               expense_of_all_per_man,  # ratio

                                        ## 가중치는 5단계(0,1,2,3,4,5) <- 가중치 0이 제외된 항목임.
               weight_lodging,          # ratio
               weight_shopping,         # ratio
               weight_food,             # ratio
               weight_transport,        # ratio
               weight_entertainment,    # ratio
               weight_culture           # ratio
               ):
    """
    input parameter:

        motive_of_tour_1
        motive_of_tour_2
        motive_of_tour_3
            range of motive_of_tour_1~3 : [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 97]

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

    motivation_code_list = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 97]
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


    output_dict = {}

    output_dict["motive_of_tour_1"] = motive_of_tour_1
    output_dict["motive_of_tour_2"] = motive_of_tour_2
    output_dict["motive_of_tour_3"] = motive_of_tour_3

    output_dict["accompany_with_alone"] \
    = output_dict["accompany_with_family"] \
    = output_dict["accompany_with_friend"] \
    = output_dict["accompany_with_colleague"] \
    = output_dict["accompany_with_etc"] = None

    if accompany_kind == 1:
        output_dict["accompany_with_alone"] = 1.0
    elif accompany_kind == 2:
        output_dict["accompany_with_family"] = 2.0
    elif accompany_kind == 3:
        output_dict["accompany_with_friend"] = 3.0
    elif accompany_kind == 4:
        output_dict["accompany_with_colleague"] = 4.0
    elif accompany_kind == 5:
        output_dict["accompany_with_etc"] = 5.0
    else:
        pass

    output_dict["num_accompany_origin"] = 1
    if accompany_num != None:
        output_dict["num_accompany_origin"] = accompany_num

    output_dict["stay_period_origin"] = stay_period
    output_dict["expense_of_all_per_man"] = expense_of_all_per_man

    output_dict["weight_lodging"] = weight_lodging
    output_dict["weight_shopping"] = weight_shopping
    output_dict["weight_food"] = weight_food
    output_dict["weight_transport"] = weight_transport
    output_dict["weight_entertainment"] = weight_entertainment
    output_dict["weight_culture"] = weight_culture


    return output_dict


def main():
    # for col_x in col_check_list_x:
    #     column_none_ratio(col_x)
    #     column_distribution_check(col_x)
    pass


main()