import sys
import os
import json
import argparse
import time
from twython import Twython
def relativepath(filename, subdirectory=''):
    dirname=os.getcwd()
    if subdirectory is not '':
        dirname=os.path.join(dirname,subdirectory)
    filepath = os.path.join(dirname, filename)
    return filepath
def jd(filename):
    filepath = relativepath(filename, 'json')
    if os.access(filepath,os.W_OK):
        with open(filepath,'r') as f:
            data = json.load(f)
        f.close()
    else:
        data = {}
    return data
def dj(data,filename):
    with open(relativepath('searchdata.json','json'),'w') as f:
        f.write(json.dumps(data))    
def sortDict(d):
    sortedkeys=sorted(d,key=d.get,reverse=True)
    sortedvalues=sorted(d.values(),reverse=True)
    newdata={}
    for i in range(len(sortedkeys)):
        newdata[sortedkeys[i]]=sortedvalues[i]
    return newdata
def addQuery(data,dictionary):
    #when keywords and values are singular
    for keyword in dictionary:
        if keyword in data:
            score=(data[keyword]+dictionary[keyword])/2.0
        else:
            score=dictionary[keyword]
        print(keyword+" : "+str(score))
        data[keyword]=score

personalinfo=jd('localInfo.json')
twitterkey=personalinfo['twitterconsumerkey']
twittersecret=personalinfo['twitterconsumersecret']
twittertoken=personalinfo['twitteraccesstoken']
twittertokensecret=personalinfo['twitteraccesstokensecret']
twitter=Twython(twitterkey,twittersecret,twittertoken,twittertokensecret)

def sentiment(words):
    dictionary={}
    keywords=[]
    if isinstance(words, str):
        keywords.append(words)
    elif all(isinstance(item, str) for item in words):
        keywords=words
    else:
        raise TypeError()

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid=SentimentIntensityAnalyzer()
    compound=0.0

    data=jd("searchdata.json")
    
    for i in range(len(keywords)):
        a=twitter.search(q=keywords[i],count=10000,lang='en')
        for j in range(len(a['statuses'])):
            compound+=sid.polarity_scores(a['statuses'][j]['text'])['compound']
        dictionary[keywords[i]]=compound
    
    addQuery(data,dictionary)
    data=sortDict(data)
    dj(data,'searchdata.json')
    return data


if __name__ == "__main__":
    if len(sys.argv)<2:
        raise SyntaxError("Please Provide a Keyword as an argument")
    else:
        words=[]
        for i in range(len(sys.argv)-1):
            words.append(sys.argv[i+1])
        sentiment(words)