import keyword_tool_functions as tools

my_list = ['how to start a business']
my_result = tools.populate_autocomplete(my_list)



for row in my_result:
    print(row)

print(len(my_result))

#my_result = list(dict.fromkeys(my_result))