import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
#1 import pandas as pd
import itertools
import requests
import string
import json
import time
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime



class Keyword:
    def __init__(self, keyword, allintitle, parent_keyword, processed, toprocess):
        self.keyword = keyword
        self.allintitle = allintitle
        self.parent_keyword = parent_keyword
        self.processed = processed
        self.toprocess = toprocess
        self.related_keywords = []
        self.autosuggest_list = []
        self.volume = -1
    

        # Creating a datetime object so we can test.
        a = datetime.now()

        # Converting a to string in the desired format (YYYYMMDD) using strftime
        # and then to int.
        a = int(a.strftime('%Y%m%d'))
 
    def __repr__(self):
        self.toJson()


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def get_data(self):
        print("Collecting keyword data for " + self.keyword )
        # This will get the data for this keyword
        # allintoitle, volume etc
        # It will also get the related keywords
        keyword_list, total_allintitle_results, keyword_to_check = get_keyword_data(self.keyword)
        self.allintitle = total_allintitle_results
        for rel_kw in keyword_list:
            self.related_keywords.append(rel_kw)
        #self.toprocess = 1
        self.processed = 1
        
    def get_autosuggest(self):
        print('Getting Autosuggest keyword Ideas for ' + self.keyword)
        kw_list = [self.keyword]
        suggested_list = populate_autocomplete(kw_list)
        #print(suggested_list)
        for sug_kw in suggested_list:
            self.autosuggest_list.append(sug_kw[1])
        print(self)
    
    def get_related_autosuggest(self, list_to_check):
        print('Getting Autosuggest keyword Ideas for ' + self.keyword)
        kw_list = list_to_check
        suggested_list = populate_autocomplete(kw_list)
        #print(suggested_list)
        for sug_kw in suggested_list:
            self.autosuggest_list.append(sug_kw[1])
        print(self)


    def __str__(self):
        return "Keyword: %s,  Allintitle: %s, parent_keyword: %s Processed: %s, ToProcess: %s" % (self.keyword, self.allintitle, self.parent_keyword, self.processed, self.toprocess)


class Report:
    def __init__(self, report_id, user_id, date_created, seed_keyword, keyword_list):
        self.report_id = uuid.uuid4()
        self.user_id = user_id
        self.date_created = int(datetime.now().strftime('%Y%m%d'))
        self.keyword_list = []
        self.seed_keyword = seed_keyword
        self.my_seed_kw = Keyword(seed_keyword,-1,'none',0,1)
        self.list_to_run_autosuggest = []

    def __str__(self):
    
        output = 'Report Id:    ' + str(self.report_id) + '\n'
        output = output + 'User Id:      ' + str(self.user_id) + '\n'
        output = output + 'Date Created: ' + str(self.date_created) + '\n'
        output = output + 'seed_keyword: ' + self.seed_keyword + '\n'
        output = output + 'Keywords:\n' 
        
        counter = 0
        for kw in self.keyword_list:
            if kw.allintitle >= 0:
                output = output + kw.keyword + ' -  Allintitle: ' + str(kw.allintitle) +  '\n'
                counter = counter + 1
        output = output + '\nOther Keyword Ideas:\n' 
        for kw in self.keyword_list:
            if kw.allintitle == -1 and counter < 100:
                output = output + kw.keyword + '\n'
                counter = counter + 1


        return output


    def add_keyword_to_list(self, kw_list):
        self.keyword_list.append(kw_list)

    def run_report(self):
        print('Starting report...')
        # get data for seed keyword
        self.my_seed_kw.get_data()
        # add seed keyword into keyword list  - processed flag is set in the get_data function
        self.keyword_list.append(self.my_seed_kw)
        # add related keywords to keyword list with toprocess flag set to 1 and processed flag set to 0
       
        
        self.list_to_run_autosuggest.append(self.my_seed_kw.keyword)

        for kw in self.keyword_list[0].related_keywords:
            #print('for kw in self.keyword_list[0].related_keywords')
            self.list_to_run_autosuggest.append(kw)
            #self.keyword_list.append(Keyword(kw,-1,'none',0,1))
        

        
        # Add in the autosuggest data
        self.my_seed_kw.get_related_autosuggest(self.list_to_run_autosuggest)

 
        for kw in self.my_seed_kw.autosuggest_list:
            #list_for_autosuggest.append(kw)
            self.keyword_list.append(Keyword(kw,-1,'none',0,1))

        

        processes = []
        counter = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            for kw in self.keyword_list:
                if counter < 10:
                    processes.append(executor.submit(get_data, kw))
                    counter = counter + 1

        for task in as_completed(processes):
            print(task.result())            


def get_data(keyword):
    keyword.get_data()   


def get_keyword_data(keyword_to_check):
    # does an allintotle keyword check on the supplied keyword
    # returns the keyword, the total results and a list of related keywords

    # set up the request parameters
    params = {
  'api_key': 'C4208DCF131C4A56A2DAB9EC31C28AED',
  'q': 'allintitle:'+ keyword_to_check,
  'output': 'json',
  'gl': 'us'
    }
    #print(params)

    # make the http GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)
    data = json.dumps(api_result.json())
     #Alternativly read from file to stop making request during development
    #with open("data_file.json", "r") as read_file:
    #    data = json.load(read_file)

    person_dict = json.loads(data)
    #keyword_list = [keyword_to_check]
    keyword_list = []

# Extract related questions and searches
    try:
        for each in person_dict['related_searches']:
            keyword_list.append(each['query'])
    except Exception:
        pass

    try:
        for each in person_dict['related_questions']:
            keyword_list.append(each['question'])
    except Exception:
        pass

# Extract the number of results
    try:
        total_allintitle_results= person_dict['search_information']['total_results']
    except Exception:
        total_allintitle_results = -2
        pass
    

    return keyword_list, total_allintitle_results, keyword_to_check






def insert_records(keyword, total_allintitle_results, processed, toprocess, volume, parent_keyword):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('keywords')
    print('Inserting Record for ' + keyword)
    print(keyword, total_allintitle_results, processed, toprocess, volume, parent_keyword)
    try: 
        conditionalUpdateResponse = table.put_item(
            Item={
            'keyword': keyword,
            'parent_keyword': parent_keyword,
            'allintitle': total_allintitle_results,
            'volume':volume,
            'last_updated': -1,
            'processed': processed,
            'toprocess': toprocess,
            },
            ConditionExpression = "attribute_not_exists(keyword)"
        )
    except ClientError as e:  
        if e.response['Error']['Code']=='ConditionalCheckFailedException':  
            print(e.response['Error']) 
            pass

def store_report(report_id, user_id, report, keyword_list):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('reports')
    print('Storing report')
    try: 
        conditionalUpdateResponse = table.put_item(
            Item={
            'report_id': report_id,
            'user_id': user_id,
            'report': report,
            'keyword_list': keyword_list,
            },
            ConditionExpression = "attribute_not_exists(report_id)"
        )
    except ClientError as e:  
        if e.response['Error']['Code']=='ConditionalCheckFailedException':  
            print(e.response['Error']) 
            pass


def populate_autocomplete(keyword_list):
    # Takes a keyword list and gets autocmplete suggestions based on the list
    # Returns a list of the origional keyword/suggestions pairs

    startTime = time.time()

    # If you use more than 50 seed keywords you should slow down your requests - otherwise google is blocking the script
    # If you have thousands of seed keywords use e.g. WAIT_TIME = 1 and MAX_WORKERS = 10

    WAIT_TIME = 0.2
    MAX_WORKERS = 10

    # set the autocomplete language
    lang = "en"

    charList = " " + string.ascii_lowercase + string.digits

    def makeGoogleRequest(query):
        # If you make requests too quickly, you may be blocked by google 
        time.sleep(WAIT_TIME)
        URL="http://suggestqueries.google.com/complete/search"
        PARAMS = {"client":"firefox",
                "hl":lang,
                "q":query}
        headers = {'User-agent':'Mozilla/5.0'}
        response = requests.get(URL, params=PARAMS, headers=headers)
        if response.status_code == 200:
            suggestedSearches = json.loads(response.content.decode('utf-8'))[1]
            #print(suggestedSearches)
            return suggestedSearches
        else:
            return "ERR"
            
    def getGoogleSuggests(keyword):
        # err_count1 = 0
        queryList = [keyword + " " + char for char in charList]
        suggestions = []
        for query in queryList:
            suggestion = makeGoogleRequest(query)
            if suggestion != 'ERR':
                suggestions.append(suggestion)
                
        # Remove empty suggestions
        suggestions = set(itertools.chain(*suggestions))
        if "" in suggestions:
            suggestions.remove("")

        return suggestions


    #read your csv file that contain keywords that you want to send to google autocomplete
    #1 df = pd.read_csv("keyword_seeds.csv")
    # Take values of first column as keywords
    #1 keywords = df.iloc[:,0].tolist()
    keywords = keyword_list

    resultList = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuresGoogle = {executor.submit(getGoogleSuggests, keyword): keyword for keyword in keywords}

    for future in concurrent.futures.as_completed(futuresGoogle):
        key = futuresGoogle[future]
        for suggestion in future.result():
            resultList.append([key, suggestion])

    # Convert the results to a dataframe
    #1 outputDf = pd.DataFrame(resultList, columns=['Keyword','Suggestion'])

    # Save dataframe as a CSV file
    #outputDf.to_csv('keyword_suggestions.csv', index=False)
    #print('keyword_suggestions.csv File Saved')

    #print(f"Execution time: { ( time.time() - startTime ) :.2f} sec")

    return resultList