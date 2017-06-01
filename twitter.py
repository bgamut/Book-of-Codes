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
