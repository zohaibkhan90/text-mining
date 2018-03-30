from urllib.request import Request, urlopen, URLError
import requests
import json

#URL, parameters and headers for nerd document call
NERD_DOCUMENT_URL = 'http://nerd.eurecom.fr/api/document'
nerd_document_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
nerd_document_data = {
	'key' : '9reqenou0oc0dop4aet49kht1eis95d5',
	'text' : '' #set text to named entities for which you need to extract the ontology
}

#URL, parameters and headers for nerd annotation call
NERD_ANNOTATION_URL = 'http://nerd.eurecom.fr/api/annotation'
nerd_annotation_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
nerd_annotation_data = {
	'key' : '9reqenou0oc0dop4aet49kht1eis95d5',
	'idDocument' : '',#set this idDocument for the document you need
	'extractor' : 'textrazor'
}

#URL and parameters for nerd entity call
idAnnotationPlaceHolder='IDANNOTATION'
key='9reqenou0oc0dop4aet49kht1eis95d5'
NERD_ENTITY_URL = str('http://nerd.eurecom.fr/api/entity?key='+key+'&idAnnotation='+idAnnotationPlaceHolder)


#URL, parameters and headers for yago annotation call
YAGO_URL = 'https://api.ambiverse.com/v2/entitylinking/analyze'
yago_headers = {'AUTHORIZATION': '2aee483f20bdfa0157da28dd3d01ed5ebbb7a31e', 'Content-Type': 'application/json'}
yago_data = {
  "coherentDocument": True,
  "confidenceThreshold": 0.075,
  "docId": "Test_Tweets",
  "text": "", #set text to named entities for which you need to extract the ontology
  "language": "en",
  "annotatedMentions": [
    {
      "charLength": 2,
      "charOffset": 0
    }
  ]
}


# takes data and returns idAnnotation for the entity 
def callNERD_documentAPI(data):
	print('calling nerd document')
	nerd_document_data['text'] = data
	try:
		response = requests.post(NERD_DOCUMENT_URL, data=nerd_document_data, headers=nerd_document_headers)
		return response.json()
	except Exception as e:
	    print ('Got an error code:'+ str(e))


# takes idDocument and returns idAnnotation for the entity 
def callNERD_AnnotationAPI(idDocument):
	print('calling nerd annotation')
	nerd_annotation_data['idDocument'] = idDocument
	try:
		response = requests.post(NERD_ANNOTATION_URL, data=nerd_annotation_data, headers=nerd_annotation_data)
		return response.json()
	except Exception as e:
	    print ('Got an error code:'+ str(e))


#takes idAnnotation and returns array for Named Entities with their ontologies
def callNERD_EntityAPI(idAnnotation):
	print('calling nerd entity')
	url = NERD_ENTITY_URL.replace(idAnnotationPlaceHolder, idAnnotation)
	request = Request(url)
	try:
		response = urlopen(request)
		data = response.read()
		return data
	except URLError as e:
	    print ('Got an error code:'+ str(e))


#returns array for Named Entities with their ontologies
def callNERD(data):
	print('calling nerd')
	try:
		response_iddocument = callNERD_documentAPI(data)
		print("Document Response: "+str(response_iddocument))
		response_idannotation = callNERD_AnnotationAPI(str(response_iddocument['idDocument']))
		print("Annotation Response: "+str(response_idannotation))
		ne_response=callNERD_EntityAPI(str(response_idannotation['idAnnotation']))
		return ne_response
	except URLError as e:
		    print ('Got an error code:'+ str(e))


#returns array for Named Entities with their ontologies
def callYAGO(data):
	print('calling yago')
	yago_data['text'] = data
	try:
		response = requests.post(YAGO_URL, json=yago_data, headers=yago_headers)
		print(response.json())
		return response.json()
	except Exception as e:
	    print ('Got an error code:'+ str(e))

# print(str(callNERD("Alvin Green")))


