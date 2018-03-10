import tweepy
import pandas as pd
####input your credentials here
consumer_key = '1unNdWtKesoQB0iOiVKOCxIDr'
consumer_secret = 'wU6FnkB0mayfR04Bxps1Fq6tFOEQsdaw17hpMznPFKNk3upETR'
access_token = '969594727308939265-uRxNPFkIacQJeg15RRJX5OdXBpYyhsi'
access_token_secret = 'NfngZtKXO424OoDErqgj2hPrUl2ulG7PqUMvFRronqRrL'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
tsvFile = open('/Users/zohaib/Desktop/Courses/Text-Mining/Data/ua.tsv', 'a')

count = 0
for tweet in tweepy.Cursor(api.search,q="#christmas",count=100,
                           lang="en",
                           since="2015-04-03").items():
    # print (tweet.created_at, tweet.text)
    count = count + 1
    if(count%10000) == 0 :
    	print ('Downloaded Tweets: '+str(count))
    if(count == 161191) :
    	break
    tsvFile.write(str(tweet.created_at) +'\t'+ str(tweet.text.encode('utf-8'))+'\n')
tsvFile.close()