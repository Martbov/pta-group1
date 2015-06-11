# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter, defaultdict
from nltk.corpus import wordnet as wn
import os, codecs, sys, urllib, json, pickle
from nltk.wsd import lesk
from nltk import word_tokenize
#from progressbar import ProgressBar

#reload(sys)
#sys.setdefaultencoding("utf-8")


def createtraindata():
	""" Creates the traindata for the NER Tagger """
	newsHandler = codecs.open('development.set','r')
	#trainData = open('traindata_all.tsv', 'a')
	#testData = open('testdata.tsv', 'a')
	newsList = []
	for line in newsHandler:
		newsList.append(line)
	#trainSplit = int(0.8 * len(newsList))
	#trainPart = newsList[:trainSplit]
	#testPart = newsList[trainSplit:]
	#createfiles(trainPart,trainData)
	#createfiles(testPart,testData)
	referenceDict = createfiles(newsList)#,trainData)
	newsHandler.close()
	#trainData.close()
	#testData.close()
	return referenceDict
	

def createfiles(Part,filename):
	""" Creates parts of the referenceDict """
	#pbar = ProgressBar()
	docId = ''
	sentenceDict = {}
	for line in Part:
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			sentenceDict[str(lineList)] = [lineList[4], lineList[6]]
			if docId != lineList[0]:
				#filename.write('\n')
				#filename.write(lineList[4]+'\t'+lineList[6]+'\n')
				docId = lineList[0]		
			#else:
				#filename.write(lineList[4]+'\t'+lineList[6]+'\n')
		elif len(lineList) > 5:
			sentenceDict[str(lineList)] = [lineList[4]]
			if docId != lineList[0]:
				#filename.write('\n')
				#filename.write(lineList[4]+'\t'+'O'+'\n')
				docId = lineList[0]		
			#else:
			#	filename.write(lineList[4]+'\t'+'O'+'\n')
	return sentenceDict

def tagdata(testData):
	""" Gives the data its NER Tags using our trained tagger """
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
			
	return taggedText, testData


def combineTags(taggedText):
	""" Adds the tags to the testfile """
	refDict=defaultdict(list)
	sentList = []
	for i, words in enumerate(taggedText):
		if i != 0:
			prevword = taggedText[i-1][0]
			prevtag = taggedText[i-1][1]
		else:
			prevword=prevtag=''
		if words[1] == prevtag:
			newTuple = (newTuple[0]+' '+words[0],words[1])
			sentList.pop()
			sentList.append(newTuple)
			refDict[i+1,words].append(newTuple)

		else: 
			newTuple = (words[0],words[1])
			sentList.append(newTuple)
			refDict[i+1,words].append(newTuple)
	print(sorted(refDict.items()))

	for i, words in enumerate(sentList):
		print(words)
		if i != 0 and i < len(sentList)-1:
			sent=sentList[i-1][0],words[0],sentList[i+1][0]
			if words[1]!= 'O':
				mwords=words[0].replace(' ','_')
				if len(wn.synsets(mwords, 'n')) > 1:
					leskDec=lesk(word_tokenize(' '.join(sent)), mwords, 'n')
					for value in refDict.values():
						if value[0] == words and len(value) < 2:
							value.append([mwords,leskDec,leskDec.definition()])
					#print(leskDec,leskDec.definition())
				else:
					for ss in wn.synsets(mwords, 'n'):
						#print(ss, ss.definition())
						for value in refDict.values():
							if value[0] == words and len(value) < 2:
								value.append([mwords,ss, ss.definition()])
	print(sorted(refDict.items()))
	return refDict
	
	
def updatedevset(referenceDict):
	""" Creates the file with NER tags """
	newsHandler = open('development.set','r')
	taggedHandler = open('nertagged.set','w')
	for line in newsHandler:
		lineList = line.strip().split()
		for key, value in referenceDict.items():
			if key == str(lineList):
				if len(value) > 1:
					if len(lineList) > 6:
						lineList.pop()
						lineList.pop()
					lineList.append(value[1])#) = lineList+' '+value[1]+'\n'
					taggedHandler.write(' '.join(lineList))
					taggedHandler.write('\n')
				else:
					lineList = lineList+'\n'
					taggedHandler.write(lineList)
	newsHandler.close()
	taggedHandler.close()

def listtags():
	""" Creates a list of NER tags """
	wordList = []
	taggedHandler = open('nertagged.set','r')
	for line in taggedHandler:
		lineItems=line.strip().split()
		if len(lineItems) > 6:
			wordList.append((str(lineItems[4]),str(lineItems[6])))
		else:
			wordList.append((lineItems[4],'O'))
	taggedHandler.close()
	#print([word for word in wordList])
	return wordList

def getwikiurls(refDict):
	""" Searches for the wikipedia links """
	#pbar = ProgressBar()
	wikiDict={}
	for key, value in pbar(refDict.items()):
		if value[0][1] != 'O' or value[0][1] != '-':
			if len(value) > 1:
				wikiresults = urllib.urlopen("http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+value[1][0]+"&format=json").read().decode('utf-8')
				wikisuggs = json.loads(wikiresults)
				for query in wikisuggs:
					for search in wikisuggs[query]:
						if search == "search":
							decisionList=[]
							for article in wikisuggs[query][search]:
								if "snippet" in article:
									x=0
									for word in article.values()[3]:
										
										if str(word) in str(value[1][2]):
											x+=1
									decisionList.append((x, article.values()[0]))
							if decisionList != []:
								bestGuess = sorted(decisionList)[-1][1]
								wikiLink= "http://en.wikipedia.org/wiki/"+bestGuess.replace(" ","_")
								wikiDict[key] = wikiLink
	return wikiDict

def addurls():
	""" Adds the wikipedia links to the file """
	urls = pickle.load(open('wikiurls.pickle','rb'))
	taggedHandler = open('nertagged.set','r')
	wikifiedHandler = open('wikitagged.set','a')
	for i, line in enumerate(taggedHandler):
		lineList=line.strip().split()
		if len(lineList) > 6 and (i+1,(lineList[4],lineList[6])) in urls.keys():
			for key in urls.keys():
				if (i+1,(lineList[4],lineList[6])) == key:
					lineList.append(str(urls.get(key)+','+str(1)))
					wikifiedHandler.write(' '.join(lineList))
					wikifiedHandler.write('\n')
		else:
			wikifiedHandler.write(' '.join(lineList))
			wikifiedHandler.write('\n')
	wikifiedHandler.close()
	taggedHandler.close()
	#urls.close()

def wikiexpander():
	""" Completes the file with missing wikipedia links """
	expandHandler = open('wikitagged.set','r')
	experiment = open('experiment.set', 'w')
	linesList = []
	for line in expandHandler:
		lineList = line.strip().split()
		linesList.append(lineList)
	prevTag = ''
	prevWiki = ''
	for line in linesList[::-1]:
		if len(line) == 6:
			experiment.write(' '.join(line))
			experiment.write('\n')
		elif len(line) > 7:
			experiment.write(' '.join(line))
			experiment.write('\n')
			prevTag = line[6]
			prevWiki = line[7]
		elif len(line) == 7:
			if line[6] == prevTag:
				line.append(prevWiki)
			else:
				link = 'http://en.wikipedia.org/'+line[4]+',1'
				line.append(link)
			experiment.write(' '.join(line))
			experiment.write('\n')
		else:
			experiment.write(' '.join(line))
			experiment.write('\n')
	expandHandler.close()
	

def reverseTagset():
	""" Reverses the tagged file to match the development set """
	experiment = open('experiment.set', 'r')
	endresult = open('finalwiki.set', 'w')
	linesList = []
	for line in experiment:
		lineList = line.strip().split()
		linesList.append(lineList)
	for line in linesList[::-1]:
		endresult.write(' '.join(line))
		endresult.write('\n')
	experiment.close()
	endresult.close()


def cleantagset(tagset):

	taggedHandler.write(' '.join(lineList))
	taggedHandler.write('\n')
	taggedHandler.close()

if __name__ == '__main__':
	referenceDict = createtraindata()
	#os.popen("java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop")
	taggedText, referenceDict = tagdata(referenceDict)
	#updatedevset(referenceDict)
	#taggedText= listtags()
	#taggedText, referenceDict = tagdata(referenceDict)
	#tagset = updatedevset(referenceDict)
	#cleantagset()
	#decidedSs=combineTags(taggedText)
	#urls=getwikiurls(decidedSs)
	#with open('wikiurls.pickle','wb') as f:
	#	pickle.dump(urls,f)
	#addurls()#urls)
	wikiexpander()
	reverseTagset()

	#wikiexpander()

