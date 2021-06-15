# Константы состояний
Q, CITY, SEX, AGE_FROM, AGE_TO, STATUS, COUNT = range(7)
par = ['q', 'city', 'sex', 'age_from', 'age_to', 'status', 'count']
key = [Q, CITY, SEX, AGE_FROM, AGE_TO, STATUS, COUNT]


def add_parameters(content, search_dic):
    for value in key:
        if content.user_data[value] != "I don't know":
            search_dic[par[value]] = content.user_data[value]
