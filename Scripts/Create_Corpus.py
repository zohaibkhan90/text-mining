#Create Corpus From Tweets

# import re
import ast
import os
import json
import time
from datetime import datetime, timedelta

max_class_limit = 10000 #max tweets to be written from a single class/event
max_general_limit = 3*max_class_limit
# max_class_limit #max tweets to be written from a single class/event
separator = ","

output_file = '/Users/zohaib/Development/workspace/text-mining/events_corpus_'+str(max_class_limit)+'.csv'
output_file_generic = '/Users/zohaib/Development/workspace/text-mining/events_corpus_generic_'+str(max_class_limit)+'.csv'
output_file_specific = '/Users/zohaib/Development/workspace/text-mining/events_corpus_specific_'+str(max_class_limit)+'.csv'

events_tweets_directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/All_Downloaded_tweets'
general_tweets_directory_path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/General_Tweets'


CSV_File_Simple = open(output_file,'w')
CSV_File_Simple.write("event"+separator+"text"+separator+"timestamp\n")
CSV_File_Generic = open(output_file_generic,'w')
CSV_File_Generic.write("event"+separator+"text"+separator+"timestamp\n")
CSV_File_Specific = open(output_file_specific,'w')
CSV_File_Specific.write("event"+separator+"text"+separator+"timestamp\n")


corpus_class = '' #name for class of an event
class_limit = 0 #number of tweets written from a single class/event
count = 0
quit = 0
US_Tweets_Started = False

initial_time = datetime.strptime('Jan 01 00:00:00 +0000 2012', '%b %d %H:%M:%S %z %Y').timestamp()
seconds_in_year = 365*24*60*60
diff = seconds_in_year/max_general_limit


ListOfFiles = []
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

generic_ontology = {}
specific_ontology = {}

def createNamedEntitiesMaps():
	ontologies_file = open('../NerdParser/parsed_set.txt','r')
	topologies = ontologies_file.readlines()
	topologies = eval(topologies[0])
	for topology in topologies:
		# print(topology)
		data = topology.split(',')
		generic_ontology[data[0]] = data[1]
		specific_ontology[data[0]] = data[2]

createNamedEntitiesMaps()

# takes a word returns most generic class for a named entity
def getGenericOntology(word):
	lower = word.lower()
	if lower.isdigit():
		return word
	if lower in generic_ontology:
		return generic_ontology[lower]
	else:
		return word

# takes a word returns most specific class for a named entity
def getSpecificOntology(word):
	lower = word.lower()
	if lower.isdigit():
		return word
	if lower in specific_ontology:
		return specific_ontology[lower]
	else:
		return word

# takes a sentence and returns with all named entities found in the sentence replaced with their most generic class
def replaceNEgeneric(sentence):
	words = sentence.split(' ')
	generic_ne_replaced_tweet = ''
	for word in words:
		generic_ne_replaced_tweet = generic_ne_replaced_tweet + ' ' + getGenericOntology(word)
	return generic_ne_replaced_tweet.strip()

# takes a sentence and returns with all named entities found in the sentence replaced with their most specific class
def replaceNEspecific(sentence):
	words = sentence.split(' ')
	specific_ne_replaced_tweet = ''
	for word in words:
		specific_ne_replaced_tweet = specific_ne_replaced_tweet + ' ' + getSpecificOntology(word)
	return specific_ne_replaced_tweet.strip()


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
			generic_ne_replaced_tweet = replaceNEgeneric(tweet_text)
			specific_ne_replaced_tweet = replaceNEspecific(tweet_text)

			CSV_File_Simple.write(corpus_class+separator+tweet_text+separator+str(date_time.timestamp())[:-2]+"\n")
			CSV_File_Generic.write(corpus_class+separator+generic_ne_replaced_tweet+separator+str(date_time.timestamp())[:-2]+"\n")
			CSV_File_Specific.write(corpus_class+separator+specific_ne_replaced_tweet+separator+str(date_time.timestamp())[:-2]+"\n")
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
			generic_ne_replaced_tweet = replaceNEgeneric(tweet_text)
			specific_ne_replaced_tweet = replaceNEspecific(tweet_text)
			initial_time = initial_time + diff
			CSV_File_Simple.write("no_event"+separator+tweet_text+separator+str(initial_time)[:-2]+"\n")
			CSV_File_Generic.write("no_event"+separator+generic_ne_replaced_tweet+separator+str(initial_time)[:-2]+"\n")
			CSV_File_Specific.write("no_event"+separator+specific_ne_replaced_tweet+separator+str(initial_time)[:-2]+"\n")
			# CSV_File_Simple.write("no_event"+separator+tweet_text+separator+str(initial_time)[:-2]+separator+datetime.fromtimestamp(initial_time).strftime('%Y-%m-%d %H:%M:%S')+"\n")
			g_limit = g_limit + 1
		if g_limit >= max_general_limit:
			print ("Completed limit for class: no_event, Total entries:" + str(g_limit))
			break
	if g_limit >= max_general_limit:
		break

CSV_File_Simple.close()
CSV_File_Generic.close()
CSV_File_Generic.close()