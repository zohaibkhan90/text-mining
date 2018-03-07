#Path to the directory to be used for saving downloaded tweets
dir_path_tweet_files = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/us_elections/us_elections/USElections_Downloaded_Tweets_batch2'
#Pattern for the file names that will be used to save the downloaded tweets in the aboove directory: example -> for value file_xxxx.txt, the generated files will be names as file_0.txt, file_1.txt, file_2.txt, file_3.txt, file_4.txt
downloaded_tweets_file_name = 'us_elections_downloaded_tweets_xxxx.txt'
#Path to the directory that contains the files for tweet ids
dir_path_tweet_ids_files = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/us_elections/us_elections/USElections_ids'


import tweepy
import os



def lookup_tweets(tweet_IDs, api):
    full_tweets = []
    tweet_count = len(tweet_IDs)
    try:
        start = 0;
        end = 0;
        for i in range((tweet_count // 100) + 1):
            # Catch the last group if it is less than 100 tweets
            end_loc = min((i + 1) * 100, tweet_count)
            start = i * 100+1
            end = end_loc
            if end%1000==0:
                print("Processed tweets: "+str(end_loc) + " out of " + str(tweet_count))
            if start<end:
                full_tweets.extend(
                    api.statuses_lookup(tweet_IDs[i * 100+1:end_loc])
                )
        return full_tweets
    except tweepy.TweepError as e:
        print ('Something went wrong, quitting... Start: '+str(start)+", End: "+str(end),str(e))

consumer_key = '1unNdWtKesoQB0iOiVKOCxIDr'
consumer_secret = 'wU6FnkB0mayfR04Bxps1Fq6tFOEQsdaw17hpMznPFKNk3upETR'
access_token = '969594727308939265-uRxNPFkIacQJeg15RRJX5OdXBpYyhsi'
access_token_secret = 'NfngZtKXO424OoDErqgj2hPrUl2ulG7PqUMvFRronqRrL'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


list_of_tweet_ids = []
completed_files = 0

file_number = 18
for filename in os.listdir(dir_path_tweet_ids_files):
    tweet_ids_file = open(dir_path_tweet_ids_files+'/'+filename,'r')
    list_of_tweet_ids = tweet_ids_file.readlines()
    tweet_ids_file.close()
    list_of_tweet_ids2 = []
    completed_files+=1
    print('Processing file number '+str(completed_files) + " with number of tweet ids = "+ str(len(list_of_tweet_ids)))
    TweetsOutputFile=open(dir_path_tweet_files+'/'+downloaded_tweets_file_name.replace("xxxx",str(file_number)),"a")
    file_number = file_number + 1
    for value in list_of_tweet_ids:
        list_of_tweet_ids2.append(value[:-1]) # removing the \n from each line (each tweet id)
    results = lookup_tweets(list_of_tweet_ids2, api)
    if results:
        for tweet in results:
            if tweet:
                # print (tweet.text)
                TweetsOutputFile.write(str(tweet._json))
                TweetsOutputFile.write('\n')
    TweetsOutputFile.close()