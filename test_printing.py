import keyword_tool_functions as tools
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from datetime import datetime
import uuid




class Report:
    def __init__(self, report_id, user_id, date_created, seed_keyword, keyword_list):
        self.report_id = uuid.uuid4()
        self.user_id = user_id
        self.date_created = int(datetime.now().strftime('%Y%m%d'))
        self.keyword_list = []
        self.seed_keyword = seed_keyword
        #self.my_seed_kw = Keyword(seed_keyword,-1,'none',0,1)
        self.list_to_run_autosuggest = []

    def __str__(self):

        output = '####################\n'+'My Report\n'+'####################\n'
        output = output + 'Report Id:    ' + str(self.report_id) + '\n'
        output = output + 'User Id:      ' + str(self.user_id) + '\n'
        output = output + 'Date Created: ' + str(self.date_created) + '\n'
        output = output + 'seed_keyword: ' + self.seed_keyword + '\n'
        output = output + 'Keywords:\n' 
        for kw in keyword_list:
            output = output + keyword


        return output

keyword_list = []
my_report = Report(123 ,456 ,'','lightgungamer', keyword_list)

print(my_report)