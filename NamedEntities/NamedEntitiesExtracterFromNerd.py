# This class calls NERD with tweets data and downloads the ontologies for named entities

import api_calls.Nerd_Yago_APIs_util as nyau
import json
input_nes = '/Users/zohaib/Development/workspace/text-mining/CleanTextFile.txt'
output_directory = '/Users/zohaib/Development/workspace/text-mining/named_entities/1/'

# lfc should be to liverpool ever.. litteringlondonwaiting to
# lfc fan should not be allowed to leave liverpool ever..
skip_words = 0
data_limit = 170000
separator = ","

nes_file = open(input_nes,'r')
output_filename = 'ne_replaced_xxxx.json'



lineString = nes_file.readlines()
nes_file.close()




s = set()


def parseNerdResponse(response):
	print("number of results: "+str(len(response)))
	for element in response:
		#do stuff
		# print(element)
		s.add(element['extractor'])
		# break


print(len(lineString))
expected_calls = int(len(lineString[0])/data_limit)
named_entities = lineString[0].split(' ')
# print(named_entities)
print(len(named_entities))
print('total characters from file: '+str(len(named_entities)))

data = ""

file_number = 0 
total_words = 0
api_calls_count=0
for named_entity in named_entities:
	if skip_words>0:
		skip_words = skip_words -1
		continue
	if len(data)>=data_limit:
		#call nerd
		response = nyau.callNERD(data)
		response = response.decode("utf-8")
		response = json.loads(response)

		# parseNerdResponse(response)

		api_calls_count = api_calls_count + 1 
		print('Number of Calls Made: '+str(api_calls_count))
		print('Expected Remaining Calls: '+str(expected_calls - api_calls_count))
		file_number = file_number + 1
		JSON_File = open(output_directory+output_filename.replace('xxxx',str(file_number)),'w')
		JSON_File.write(str(response))
		JSON_File.close()
		print('Skip Words Next time: '+str(total_words))
		print('Skip after this sequence: '+data[-50:]) 
		#clear data
		data = ""
		# break
	else:
		total_words = total_words + 1
		data = data + " " + named_entity

if len(data)>0:
	response = nyau.callNERD(data)
	response = response.decode("utf-8")
	response = json.loads(response)

	# parseNerdResponse(response)

	api_calls_count = api_calls_count + 1 
	print('Number of Calls Made: '+str(api_calls_count))
	print('Expected Remaining Calls: '+str(expected_calls - api_calls_count))
	file_number = file_number + 1
	JSON_File = open(output_directory+output_filename.replace('xxxx',str(file_number)),'w')
	JSON_File.write(str(response))
	JSON_File.close()
	print('Skip Words Next time: '+str(total_words))
	print('Skip after this sequence: '+data[-50:]) 
	#clear data
	data = ""


