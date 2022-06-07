import boto3
from boto3.dynamodb.conditions import Key
import json
import keyword_tool_functions as tools


def query_keywords(dynamodb=None):
   # if not dynamodb:
    #    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('keywords')

    response = table.query(
        IndexName="allintitle-index",
        KeyConditionExpression=Key('allintitle').eq(-1)
    )

 


    return response


if __name__ == '__main__':
 
 
    keywords = query_keywords()
    #keywords_dict = json.loads(keywords)
    #for keyword in keywords_dict:
    #    print(keyword['keyword'], ":", keyword['allintitle'])
    for i in keywords['Items']:
        print(i['keyword'], ":", i['allintitle'])

        keyword_list, total_allintitle_results, keyword = tools.get_keyword_data(i['keyword'])

        #new_list = populate_autocomplete(keyword_list)

        #keyword = 'how to drive traffic'
        #total_allintitle_results = 15000
        processed = 1 
        toprocess = 0
        volume = -1
        parent_keyword = ''
        tools.insert_records(keyword, total_allintitle_results, processed, toprocess, volume, parent_keyword)

        for kw in keyword_list:
            tools.insert_records(kw, -1, 0, 0, -1, keyword)
   # print(keywords)