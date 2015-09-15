# -*- coding:utf-8 -*-
"""
    author: ming (k239507@gmail.com)

    function: read code mapping csv file (code, eng_code, ko_code map table like)
        and examination for foreign visit excel file, then rename the column name of excel
	to readable english code name.   
"""

import pandas as pd

code_file_path = "../code-book/"
data_source_file_path = "../data-source/"
data_result_file_path = "../data-result/"

code_csv = pd.read_csv(code_file_path + \
    u'code-book-for-foreign-tourist-research-2014.csv')
data_xl = pd.read_excel(data_source_file_path + \
    u'2014년 외래관광객 실태조사 원자료.xlsx')

code_match_dict = {}

for row in code_csv.iterrows():
    code_match_dict[row[1][0]] = row[1][1]

for key, value in code_match_dict.items():
    if key in data_xl:
	data_xl[value] = data_xl.pop(key)

# renamed excel dataframe to csv file
data_xl.to_csv(data_result_file_path + \
    'eng_code_mapped_csv.csv')

# renamed excel dataframe to excel file
data_xl.to_excel(data_result_file_path + \
    'eng_code_mapped_excel.xlsx', sheet_name="Examination of foreign visit")

