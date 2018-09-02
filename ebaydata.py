from ebaysdk.finding import Connection as finding
import sentiment as s
import math
keyword='supreme'
searchNumber=10
entriesPerPage=25
totalPageNumber=math.ceil(searchNumber/entriesPerPage)
api=finding(appid =s.jd('localInfo.json')['ebayappid'], config_file=None)
price=0
dictionary={}
for i in range(totalPageNumber):
    api.execute('findItemsAdvanced', {
        'keywords': keyword,
        'itemFilter': [
            {'name': 'Condition', 'value': 'Used'},
                    {'name': 'MinPrice', 'value': '10', 'paramName': 'Currency', 'paramValue': 'USD'},
            {'name': 'MaxPrice', 'value': '1000000', 'paramName': 'Currency', 'paramValue': 'USD'}
        ],
        'paginationInput': {
            'entriesPerPage': entriesPerPage,
            'pageNumber': i+1
            },
        'sortOrder': 'CurrentPriceHighest'
        })

    dict=api.response_dict()
    
    
    for j in range(entriesPerPage):
        category=str(dict.searchResult.item[j].primaryCategory.categoryName)
        if category not in dictionary:
            dictionary[category]=[]
        print(dict.searchResult.item[j])
        dictionary[category].append(float(dict.searchResult.item[j].sellingStatus.currentPrice.value))
        #print(" ")

#responsedataobject is not subscriptable 
"""
    for j in range(entriesPerPage):
        if str(dict['searchResult']['item'][j]['categoryName']) not in categories:
            categories.append(dict['searchResult']['item'][i]['categoryName'])
        price += dict['searchResult']['item'][j]['currentPrice']['value']
"""
for key in dictionary:
    average_price=0
    for i in range(len(dictionary[key])):
        average_price+=dictionary[key][i]
    dictionary[key]=average_price
    
print(dictionary)

