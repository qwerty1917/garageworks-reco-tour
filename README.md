# garageworks-reco-tour


###### this is recommendation system (service) for foreign tourist (in korea yet)
--

### directory description
- code-book : column, key code table (include description)
- data-source : any data source (like csv, xlsx etc ...)
- data-result : if you work with data for analyzing, handling, converting, etc, then save the result (file, text ... any type) in this folder

--

### pending issues
- ordinal 변수들의 가중치가 지나치게 큼(+- 10 정도. 다른변수들은 1 ~ 3)
- 실행시간 문제로 표본을 랜덤하게 추출중이라 같은조건에서 실행시마다 결과값이 달라짐 
- ordinal 변수 grade 계산할때 6개 인자 모두에 대해서 계산하고 있음. 기획이 그대로 3개만 선택하는 것이라면 앞의 3개씩만 계산하도록 고쳐야함.

--