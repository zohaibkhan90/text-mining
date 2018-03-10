#Create Corpus From Tweets

import re
import ast

output_file = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/events_corpus.tsv'
directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/All_Downloaded_tweets'

TSV_File = open(output_file,'w')
TSV_File.write("Class\tText\n")

# max_class_limit = 161190 #max tweets to be written from a single class/event
max_class_limit = 100 #max tweets to be written from a single class/event
corpus_class = '' #name for class of an event
class_limit = 0 #number of tweets written from a single class/event
for filename in os.listdir(directory_path):
	if filename.contains('fa_cup_downloaded_tweets'):
		corpus_class = 'Fifa_Final'
	else if filename.contains('super_tuesday_data'):
		corpus_class = 'Super_Tuesday'
	else if filename.contains('us_elections_downloaded_tweets'):
		corpus_class = 'Super_Tuesday'
    tweets_file = open(directory_path+'/'+filename,'r')
    lineString = tweets_file.readlines()
    print ('running file: '+str(filename) + ' with corpus class: '+ str(corpus_class))
	for value in lineString:
		class_limit = class_limit + 1
	    json_str = ast.literal_eval(value)
	    # print ("id str: "+json_str['id_str'])
	    # print ("id str: "+json_str['created_at'])
	    # print ("origional text: "+json_str['text'])
	    # print ("processed text: "+processTweet2(json_str['text']))    
	    count = count + 1
	    if count%10000==0:
	        print ("Tweets Written: "+ str(count))
	        print ("Total Tweets from class: "+corpus_class +': '+ str(class_limit))
	    if json_str['lang'] == 'en':
	        TSV_File.write(corpus_class+"\t"+json_str['text']+"\n")
		if class_limit <= max_class_limit:
			print ("Completed limit for class: "+corpus_class +', Total entries: '+ str(class_limit))
			class_limit = 0
			break
    

TSV_File.close()

