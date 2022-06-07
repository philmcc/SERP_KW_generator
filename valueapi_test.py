import requests
import json


keyword_to_check = 'how to market your house cleaning business'
# set up the request parameters
params = {
  'api_key': 'C4208DCF131C4A56A2DAB9EC31C28AED',
  'q': 'allintitle:'+keyword_to_check,
  'output': 'json',
  'gl': 'us'
}

# make the http GET request to VALUE SERP
#api_result = requests.get('https://api.valueserp.com/search', params)
#data = json.dumps(api_result.json())
#Alternativly read from file to stop making request during development
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