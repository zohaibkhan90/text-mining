#Create Corpus From Tweets

# import re
import ast
import os
import json
import time
from datetime import datetime, timedelta
# output_file = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/events_corpus_6k.csv'
output_file = '/Users/zohaib/Development/workspace/text-mining/events_corpus_10000.csv'

events_tweets_directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/All_Downloaded_tweets'
general_tweets_directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/General_Tweets'

separator = ","
CSV_File = open(output_file,'w')
CSV_File.write("event"+separator+"text"+separator+"timestamp\n")

max_class_limit = 10000 #max tweets to be written from a single class/event
max_general_limit = 3*max_class_limit
# max_class_limit = 100 #max tweets to be written from a single class/event
corpus_class = '' #name for class of an event
class_limit = 0 #number of tweets written from a single class/event
count = 0
quit = 0
US_Tweets_Started = False

ListOfFiles = []

initial_time = datetime.strptime('Jan 01 00:00:00 +0000 2012', '%b %d %H:%M:%S %z %Y').timestamp()
seconds_in_year = 365*24*60*60
diff = seconds_in_year/max_general_limit

def readDirectory (dir_path): #recursivelt reads directory for general tweets and adds all files paths in a list
	# print("Directory Path is "+dir_path)
	if os.path.isdir(dir_path):
		for x in os.walk(dir_path):
			for z in x[1]: #for all directories
				# print("recursive call with path: "+x[0]+"/"+z)
				readDirectory(x[0]+"/"+z)
			for z in x[2]: #for all files
				if x[0]+"/"+z not in ListOfFiles and z != ".DS_Store": # let not the files repeat and ignore the .DS_Store file of Mac OS
					# print("Final Path to File: "+x[0]+"/"+z)
					ListOfFiles.append(x[0]+"/"+z)
readDirectory(general_tweets_directory_path)


for filename in os.listdir(events_tweets_directory_path):
	if 'fa_cup_downloaded_tweets' in filename:
		corpus_class = 'fifa_final'
	elif 'super_tuesday_data' in filename:
		corpus_class = 'super_tuesday'
	elif 'us_elections_downloaded_tweets' in filename:
		US_Tweets_Started = True
		corpus_class = 'us_elections'
		if quit == 1:
			break
	tweets_file = open(events_tweets_directory_path+'/'+filename,'r')
	lineString = tweets_file.readlines()
	tweets_file.close()
	print ('running file: '+str(filename) + ' with corpus class: '+ str(corpus_class))
	for value in lineString:
		json_str = ast.literal_eval(value)
		count = count + 1

		if count%10000==0:
			print ("Tweets Read: "+ str(count))
			print ("Total Tweets from class: "+corpus_class +': '+ str(class_limit))
		if json_str['lang'] == 'en':
			class_limit = class_limit + 1
			tweet_text = json_str['text'].replace('\r',' ')
			tweet_text = tweet_text.replace('\n',' ')
			tweet_text = tweet_text.replace(separator,' ')
			tweet_text = tweet_text.replace('RT ','')
			# print('TWEET: '+tweet_text)
			date_time = datetime.strptime(json_str['created_at'][4:], '%b %d %H:%M:%S %z %Y')
			
			CSV_File.write(corpus_class+separator+tweet_text+separator+str(date_time.timestamp())[:-2]+"\n")
			# 177078285476438017
		if class_limit >= max_class_limit:
			print ("Completed limit for class: "+corpus_class +', Total entries: '+ str(class_limit))
			if US_Tweets_Started:
				quit = 1
			class_limit = 0
			break
g_limit = 0
for file in ListOfFiles:
	print("Reading general tweets File: "+file)
	tweets_file = open(file,'r')
	lineString = tweets_file.readlines()
	tweets_file.close()
	for value in lineString:
		json_str = json.loads(value)
		if 'lang' in json_str and json_str['lang'] == 'en':
			tweet_text = json_str['text'].replace('\r',' ')
			tweet_text = tweet_text.replace('\n',' ')
			tweet_text = tweet_text.replace(separator,' ')
			tweet_text = tweet_text.replace('RT ','')
			initial_time = initial_time + diff
			CSV_File.write("no_event"+separator+tweet_text+separator+str(initial_time)[:-2]+"\n")
			# CSV_File.write("no_event"+separator+tweet_text+separator+str(initial_time)[:-2]+separator+datetime.fromtimestamp(initial_time).strftime('%Y-%m-%d %H:%M:%S')+"\n")
			g_limit = g_limit + 1
		if g_limit >= max_general_limit:
			print ("Completed limit for class: no_event, Total entries:" + str(g_limit))
			break
	if g_limit >= max_general_limit:
		break
CSV_File.close()