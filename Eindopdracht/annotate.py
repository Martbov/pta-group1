# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter
from nltk.corpus import wordnet as wn
import os, codecs
from nltk.wsd import lesk
from nltk import word_tokenize

def createtraindata():
	newsHandler = codecs.open('development.set','r')
	trainData = open('traindata_all.tsv', 'a')
	#testData = open('testdata.tsv', 'a')
	newsList = []
	for line in newsHandler:
		newsList.append(line)
	#trainSplit = int(0.8 * len(newsList))
	#trainPart = newsList[:trainSplit]
	#testPart = newsList[trainSplit:]
	#createfiles(trainPart,trainData)
	#createfiles(testPart,testData)
	referenceDict = createfiles(newsList,trainData)
	newsHandler.close()
	trainData.close()
	#testData.close()
	return referenceDict
	

def createfiles(Part,filename):
	#pbar = ProgressBar()
	docId = ''
	sentenceDict = {}
	for line in Part:
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			sentenceDict[str(lineList)] = [lineList[4], lineList[6]]
			if docId != lineList[0]:
				filename.write('\n')
				filename.write(lineList[4]+'\t'+lineList[6]+'\n')
				docId = lineList[0]		
			else:
				filename.write(lineList[4]+'\t'+lineList[6]+'\n')
		elif len(lineList) > 5:
			sentenceDict[str(lineList)] = [lineList[4]]
			if docId != lineList[0]:
				filename.write('\n')
				filename.write(lineList[4]+'\t'+'O'+'\n')
				docId = lineList[0]		
			else:
				filename.write(lineList[4]+'\t'+'O'+'\n')
	return sentenceDict

def tagdata(testData):
	tokens = []
	testData = codecs.open('testdata.tsv', 'r')
	for line in testData.values():
		tokens.append(line[0])
		if len(line) > 1:
			token = line.strip().split()
			tokens.append(token[0])
	os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
	path="ner"
	classifier = "ner-pta.ser.gz"
	jar = "stanford-ner.jar"
	tagger = NERTagger(classifier, jar)
	taggedText = tagger.tag(tokens)
	for line in taggedText:
		for value in testData.values():
			if line[0][0] == value [0]:
				value = line
	print(taggedText)
			
	return taggedText, testData


def combineTags(taggedText):
	for sentence in taggedText:
		print(sentence)
		sentList = []
		for i, words in enumerate(sentence):
			if i != 0:
				prevword = sentence[i-1][0]
				prevtag = sentence[i-1][1]
			else:
				prevword=prevtag=''
			if words[1] == prevtag:
				newTuple = (newTuple[0]+' '+words[0],words[1])
				sentList.pop()
				sentList.append(newTuple)
			else: 
				newTuple = (words[0],words[1])
				sentList.append(newTuple)
		print(sentList)

		for i, words in enumerate(sentList):
			if i != 0 and i < len(sentList)-1:
				sent=sentList[i-1][0],words[0],sentList[i+1][0]
				if words[1]!= 'O':
					if len(wn.synsets(words[0], 'n')) > 1:
						leskDec=lesk(word_tokenize(' '.join(sent)), words[0], 'n')
						pass#print(words[0], words[1])#,leskDec,leskDec.definition())
					else:
						for ss in wn.synsets(words[0], 'n'):
							pass#print(words[0],words[1])#, ss, ss.definition())
				else:
					pass#print(words[0])
	
def updatedevset(referenceDict):
	newsHandler = open('development.set','r')
	taggedHandler = open('nertagged.set','w')
	for line in newsHandler:
		lineList = line.strip().split()
		for key, value in referenceDict.items():
			if key==str(lineList):
				if len(value) > 1:
					lineList.append(value[1])#) = lineList+' '+value[1]+'\n'
					taggedHandler.write(' '.join(lineList))
					taggedHandler.write('\n')
				else:
					lineList = lineList+'\n'
					taggedHandler.write(lineList)
	newsHandler.close()
	taggedHandler.close()


def getwikiurls():
	wordList = []
	taggedHandler = open('nertagged.set','r')
	for line in taggedHandler:
		lineItems=line.strip().split()
		if len(lineItems) > 6:
			wordList.append((str(lineItems[4]),str(lineItems[6])))
		else:
			wordList.append((lineItems[4],'O'))
	taggedHandler.close()
	return wordList


def cleantagset(tagset):
	pass



if __name__ == '__main__':
	referenceDict = createtraindata()
	#os.popen("java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop")
	#taggedText, referenceDict = tagdata(referenceDict)
	#updatedevset(referenceDict)
	taggedText= getwikiurls()
	#taggedText, referenceDict = tagdata(referenceDict)
	#tagset = updatedevset(referenceDict)
	#cleantagset()

	combineTags(taggedText)


