from ebaysdk.finding import Connection as finding
import sentiment as s
import math
keyword='supreme'
searchNumber=1000
entriesPerPage=25
totalPageNumber=math.ceil(searchNumber/entriesPerPage)
api=finding(appid =s.jd('localInfo.json')['ebayappid'], config_file=None)
price=0
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
    categories=[]
    
    for j in range(entriesPerPage):
        if str(dict.searchResult.item[j].primaryCategory.categoryName) not in categories:
            categories.append(str(dict.searchResult.item[j].primaryCategory.categoryName))
        print(dict.searchResult.item[j])
        price += float(dict.searchResult.item[j].sellingStatus.currentPrice.value)
        print(" ")
#responsedataobject is not subscriptable 
"""
    for j in range(entriesPerPage):
        if str(dict['searchResult']['item'][j]['categoryName']) not in categories:
            categories.append(dict['searchResult']['item'][i]['categoryName'])
        price += dict['searchResult']['item'][j]['currentPrice']['value']
"""
    

