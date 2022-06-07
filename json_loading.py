
import json
#from extract import json_extract
import pandas as pd


with open("data_file.json", "r") as read_file:
    data = json.load(read_file)


person_dict = json.loads(data)
keyword_list = []

for each in person_dict['related_searches']:
    keyword_list.append(each['query'])

for each in person_dict['related_questions']:
    keyword_list.append(each['question'])

total_results= person_dict['search_information']['total_results']
print(keyword_list)
print(total_results)

for keyword in keyword_list:
    print(keyword)