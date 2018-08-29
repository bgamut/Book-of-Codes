"""
from tweepy import OAuthHandler
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
consumer_key='xZJ04IzBe1w4ZjEIPlDEpxmp9'
consumer_secret='xjejLpwPuZk6poRi7eH0xYSslLVtGoOh0uzgihSf8efdBQSTyb'
sid=SentimentIntensityAnalyzer()
auth=OAuthHandler(consumer_key,consumer_secret)
api=tweepy.API(auth)
search="kpop"
compound=0.0
positive=0.0
negative=0.0
list=[]
query=api.search(search,count=10000)
for i in range(len(query)):
    a=query[i]._json[u'text']
    list.append(a.encode('ascii','ignore'))
    compound+=sid.polarity_scores(a.encode('ascii','ignore'))['compound']
    positive+=sid.polarity_scores(a.encode('ascii','ignore'))['pos']
print (positive)
print (negative)
"""
import os
import json
def relativepath(filename, subdirectory=''):
    dirname=os.getcwd()
    if subdirectory is not '':
        dirname=os.path.join(dirname,subdirectory)
    filepath = os.path.join(dirname, filename)
    #print(filepath)
    return filepath
def jd(filename):
    filepath = relativepath(filename, 'json')
    #print(filepath)
    with open(filepath) as f:
        data = json.load(f)
    f.close()
    return data
f=jd('localInfo.json')

youtubetokenresponse=f['youtubetokenresponse']
bearertoken=f['bearertoken']
twitterkey=f['twitterconsumerkey']
twittersecret=f['twitterconsumersecret']
twittertoken=f['twitteraccesstoken']
twittertokensecret=f['twitteraccesstokensecret']
from twython import Twython
twitter=Twython(twitterkey,twittersecret,twittertoken,twittertokensecret)
client_args={
    'headers':{
        'q':'nasa'
    }
}
a=twitter.search(q='trap music',count=100,lang='en')
with open('searchdata.json','w') as f:
    f.write(json.dumps(a))
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid=SentimentIntensityAnalyzer()
compound=0.0
positive=0.0
negative=0.0
list=[]
for i in range(len(a['statuses'])):
    """
    print('url: '+str(a['statuses'][i]['user']['url']))
    print('')
    print(a['statuses'][i]['text'])
    print('')
    print('retweet: '+str(a['statuses'][i]['retweet_count']))
    print('')
    print('favorited: '+str(a['statuses'][i]['favorite_count']))
    print('freinds: '+str(a['statuses'][i]['user']['friends_count']))
    print('hometown: '+str(a['statuses'][i]['user']['location']))
    print('geo enabled: '+str(a['statuses'][i]['user']['geo_enabled']))
    print('time zone: '+str(a['statuses'][i]['user']['time_zone']))
    print('description: '+str(a['statuses'][i]['user']['description']))
    print('screen_name: '+str(a['statuses'][i]['user']['screen_name']))
    """
    list.append(a['statuses'][i]['text'])
    compound+=sid.polarity_scores(a['statuses'][i]['text'])['compound']
    positive+=sid.polarity_scores(a['statuses'][i]['text'])['pos']

print(list)
print('')
print ("positive: "+str(positive))
