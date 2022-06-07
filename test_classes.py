import keyword_tool_functions as tools
import time
#from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

       
startTime = time.time()        
keyword_list = []

# Initialize the report
my_report = tools.Report(123 ,456 ,'','house of the dead', keyword_list)
# run the report
my_report.run_report()

# Store the keywords in the db.
 
print('Storing keyword Data in database.')
for kw in my_report.keyword_list:
    #print(kw)
    # Only store kw based on allintitle (-2 = error, -1 = not processed yet, 0 or more is the actual allintitle number) 
    if kw.allintitle >= 0:
        tools.insert_records(kw.keyword, kw.allintitle, kw.processed, kw.toprocess, kw.volume, kw.parent_keyword)

keyword_list_json = json.dumps(my_report.keyword_list, default=lambda o: o.__dict__, indent=4)

tools.store_report(str(my_report.report_id), str(my_report.user_id), str(my_report), str(keyword_list_json))

print(my_report)
print(len(my_report.keyword_list))
print(f"Execution time: { ( time.time() - startTime ) :.2f} sec")