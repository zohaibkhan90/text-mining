import sys
import os
import itertools
import operator
import json
import ast

if len(sys.argv) < 3:
    print('Less arguments provided')
    print('Usage: python ner.py <input_dir> <output_file>')
    sys.exit(1)

if len(sys.argv) > 3:
    print('Too many arguments provided')
    print('Usage: python ner.py <input_dir> <output_file>')
    sys.exit(1)

input_nes = 'input/ne_replaced1_.json'
input_dir = sys.argv[1]
output_file = sys.argv[2]

csvSet = set()

def most_common(L):
	# get an iterable of (item, iterable) pairs
	SL = sorted((x, i) for i, x in enumerate(L))
	# print 'SL:', SL
	groups = itertools.groupby(SL, key=operator.itemgetter(0))
	# auxiliary function to get "quality" for an item
	def _auxfun(g):
		item, iterable = g
		count = 0
		min_index = len(L)
		for _, where in iterable:
			count += 1
			min_index = min(min_index, where)
		# print 'item %r, count %r, minind %r' % (item, count, min_index)
		return count, -min_index
	# pick the highest-count/earliest item
	return max(groups, key=_auxfun)[0]

def getOntology(extractorType):
	ontologyList = extractorType.split(',')

	if len(ontologyList)==1:
		if len(ontologyList[0].split('/'))==1:
			return (ontologyList[0], ontologyList[0])

	mostGeneral = []
	mostSpecific = []

	for ontology in ontologyList:
		classes = ontology.split('/')

		if classes[0]=='':
			classes.pop(0)

		mostGeneral.append(classes[0])
		mostSpecific.append(classes[len(classes)-1])

	mostCommonElement = most_common(mostGeneral)
	mostCommonIndex = mostGeneral.index(mostCommonElement)

	return (mostGeneral[mostCommonIndex], mostSpecific[mostCommonIndex])

def parseNerdResponse(arrayResponse):
	for element in arrayResponse:
		string = ''
		string += element['label'] + ','
		
		if element['extractorType'] != 'null':
			tuple = getOntology(element['extractorType'])
			string = string + tuple[0] + ',' + tuple[1]
		else:
			split = element['nerdType'].split('#')
			string = string + split[len(split)-1] + ',' + split[len(split)-1]

		csvSet.add(string)

# MAIN PROGRAM
for filename in os.listdir(input_dir):
	file = open(input_dir+'/'+filename,'r')
	listLines = file.readlines()
	file.close()

	for line in listLines:
	    arrayResponse = ast.literal_eval(line)
	    parseNerdResponse(arrayResponse)


print('Total:' + str(len(csvSet)) )

outputFile = open(output_file,'w')
outputFile.write(str(csvSet))
outputFile.close()
sys.exit(0)