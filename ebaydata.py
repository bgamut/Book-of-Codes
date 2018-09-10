from ebaysdk.finding import Connection as finding
from sentiment import *
import math
import sys
from pprint import pprint
import numpy as np
# gets a response
"""         
{'itemId': '263788452134', 
'title': "Giuseppe Zanotti E800154 Heels - Women's Size 9.5 M, Haribo Metal Multicolored", 
'globalId': 'EBAY-US', 
'primaryCategory': {'categoryId': '55793', 'categoryName': 'Heels'}, 
'galleryURL': 'http://thumbs3.ebaystatic.com/m/m7Nhon_4UfK9Ga_6V7TErBg/140.jpg', 
'viewItemURL': 'http://www.ebay.com/itm/Giuseppe-Zanotti-E800154-Heels-Womens-Size-9-5-M-Haribo-Metal-Multicolored-/263788452134', 
'paymentMethod': 'PayPal', 
'autoPay': 'true', 
'postalCode': '28092', 
'location': 'Lincolnton,NC,USA', 
'country': 'US', 
'shippingInfo': {'shippingServiceCost': {'_currencyId': 'USD', 'value': '0.0'}, 
                'shippingType': 'Free', 
                'shipToLocations': 'Worldwide', 
                'expeditedShipping': 'true', 
                'oneDayShippingAvailable': 
                'false', 
                'handlingTime': '1'}, 
'sellingStatus': {'currentPrice': {'_currencyId': 'USD', 'value': '297.75'}, 
                'convertedCurrentPrice': {'_currencyId': 'USD', 'value': '297.75'}, 
                'sellingState': 'Active', 
                'timeLeft': 'P24DT15H7M59S'}, 
                'listingInfo': {'bestOfferEnabled': 'false', 
                'buyItNowAvailable': 'false', 
                'startTime': datetime.datetime(2018, 6, 30, 15, 14, 7), 
                'endTime': datetime.datetime(2018, 9, 28, 15, 14, 7), 
                'listingType': 'StoreInventory', 
                'gift': 'false', 
                'watchCount': '6'}, 
                'returnsAccepted': 'true', 
                'condition': {'conditionId': '3000', 'conditionDisplayName': 'Pre-owned'}, 
                'isMultiVariationListing': 'false', 'topRatedListing': 'true'}
"""

def ebay(keyword):
    keyword=keyword
    searchNumber=1000
    entriesPerPage=25
    totalPageNumber=math.ceil(searchNumber/entriesPerPage)
    api=finding(appid =jd('localInfo.json')['ebayappid'], config_file=None)
    dictionary={}
    examples={}
    urls={}
    shipping={}
    flux={}
    volatility={}
    maxprices={}
    for i in range(totalPageNumber):
        api.execute('findItemsAdvanced', {
            'keywords': keyword,
            'itemFilter': [
                {'name': 'Condition', 'value': 'Used'},
                {'name': 'MinBids','value':'1'},
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MinPrice', 'value': '1', 'paramName': 'Currency', 'paramValue': 'USD'},
                {'name': 'MaxPrice', 'value': '1000000', 'paramName': 'Currency', 'paramValue': 'USD'}
            ],
            'paginationInput': {
                'entriesPerPage': entriesPerPage,
                'pageNumber': i+1
                },
            'sortOrder': 'BidCountMost'
            })

        dict=api.response_dict()
        
        
        for j in range(entriesPerPage):
            try:
                category=str(dict.searchResult.item[j].primaryCategory.categoryId+" - "+dict.searchResult.item[j].primaryCategory.categoryName)
                if category not in dictionary:
                    dictionary[category]=[]
                    shipping[category]=[]
                    examples[category]=[]
                    urls[category]=[]
                #print(dict.searchResult.item[j])
                try:
                    dictionary[category].append(float(dict.searchResult.item[j].sellingStatus.currentPrice.value))
                    examples[category].append(dict.searchResult.item[j].title)
                    urls[category].append(dict.searchResult.item[j].viewItemURL)
                    if (dict.searchResult.item[j].shippingInfo.shippingServiceCost.value=='USD'):
                        shipping[category].append(float(dict.searchResult.item[j].shippingInfo.shippingServiceCost.value))
                    #dictionary[category].append(dict.searchResult.item[j].sellingStatus.currentPrice.value+" USD")
                
                except:
                    pass
                #print(" ")
            except:
                pass

    #responsedataobject is not subscriptable 
    """
        for j in range(entriesPerPage):
            if str(dict['searchResult']['item'][j]['categoryName']) not in categories:
                categories.append(dict['searchResult']['item'][i]['categoryName'])
            price += dict['searchResult']['item'][j]['currentPrice']['value']
    """
    
    for key in shipping:
        average_shipping=0
        for i in range(len(shipping[key])):
            average_price+=shipping[key][i]/len(shipping[key])
        shipping[key]=math.floor(average_shipping)
    
    for key in dictionary:
        maxindex = np.argmax(dictionary[key])
        examples[key]=examples[key][maxindex]
        urls[key]=urls[key][maxindex]
        maxprice=math.floor(dictionary[key][maxindex])
        maxprices[key]=maxprice
        average_price=0
        flux[key]=len(dictionary[key])
        for i in range(len(dictionary[key])):
            average_price+=dictionary[key][i]/len(dictionary[key])
        dictionary[key]=math.floor(average_price)
        volatility[key]=flux[key]*(dictionary[key]-shipping[key])
    dictionary=sortDict(dictionary)
    volatility=sortDict(volatility)
    #print(dictionary)
    #new_dictionary={}
    """
    index=0
    for key in dictionary.copy():
        if index>9:
            dictionary.pop(key)
        index+=1
    """
    index=0
    for key in volatility.copy():
        if index>9:
            volatility.pop(key)
        index+=1
    #print(dictionary)
    index=1
    newExample=[]
    
    #for key in dictionary:
    for key in volatility:
        print("#"+str(index))
        print("  Category : "+key)
        print("  MAXIMUM PRICE : "+str(maxprices[key])+" USD")
        print("  AVERAGE PRICE : "+str(dictionary[key])+" USD")
        print("  AVERAGE PRICE-AVERAGE SHIPPING : "+str(dictionary[key]-shipping[key])+" USD")
        print("  volume: "+str(flux[key]))
        print("  EXAMPLE Title: "+examples[key])
        print("  EXAMPLE URL : "+urls[key])
        newExample.append(examples[key])
        index+=1
    #print(new_dictionary)
    return dictionary

        

if __name__ == "__main__":
    if len(sys.argv)<2:
        raise SyntaxError("Please Provide a Keyword as an argument")
    else:
        words=[]
        for i in range(len(sys.argv)-1):
            words.append(sys.argv[i+1])
            ebay(sys.argv)