#Create Corpus From Tweets

# import re
import ast
import os

output_file = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/events_corpus.tsv'
directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/All_Downloaded_tweets'

TSV_File = open(output_file,'w')
TSV_File.write("Class\tText\n")

max_class_limit = 161190 #max tweets to be written from a single class/event
# max_class_limit = 100 #max tweets to be written from a single class/event
corpus_class = '' #name for class of an event
class_limit = 0 #number of tweets written from a single class/event
count = 0
quit = 0
US_Tweets_Started = False
for filename in os.listdir(directory_path):
	if 'fa_cup_downloaded_tweets' in filename:
		corpus_class = 'Fifa_Final'
	elif 'super_tuesday_data' in filename:
		corpus_class = 'Super_Tuesday'
	elif 'us_elections_downloaded_tweets' in filename:
		US_Tweets_Started = True
		corpus_class = 'US_Elections'
		if quit == 1:
			break
	tweets_file = open(directory_path+'/'+filename,'r')
	lineString = tweets_file.readlines()
	print ('running file: '+str(filename) + ' with corpus class: '+ str(corpus_class))
	for value in lineString:
		json_str = ast.literal_eval(value)
		count = count + 1

		if count%10000==0:
			print ("Tweets Read: "+ str(count))
			print ("Total Tweets from class: "+corpus_class +': '+ str(class_limit))
		if json_str['lang'] == 'en':
			class_limit = class_limit + 1
			tweet_text = json_str['text'].replace('\n',' ')
			# print('TWEET: '+tweet_text)
			TSV_File.write(corpus_class+"\t"+tweet_text+"\n")
		if class_limit >= max_class_limit:
			print ("Completed limit for class: "+corpus_class +', Total entries: '+ str(class_limit))
			if US_Tweets_Started:
				quit = 1
			class_limit = 0
			break
TSV_File.close()