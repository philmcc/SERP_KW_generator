import keyword_tool_functions as tools

def main():
    
    #keyword_list, total_allintitle_results, keyword = tools.get_keyword_data('how to market a cleaning business')

    #new_list = populate_autocomplete(keyword_list)

    keyword = 'great commercial cleaning marketing ideas'
    total_allintitle_results = -1
    processed = 1 
    toprocess = 0
    volume = -1
    parent_keyword = ''
    tools.insert_records(keyword, total_allintitle_results, processed, toprocess, volume, parent_keyword)

    #for kw in keyword_list:
    #    tools.insert_records(kw, -1, 0, 0, -1, keyword)

if __name__ == "__main__":
    main()