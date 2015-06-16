# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter, defaultdict
from nltk.corpus import wordnet as wn
import os, codecs, sys, urllib.request, json, pickle
from nltk.wsd import lesk
from nltk import word_tokenize
from progressbar import ProgressBar

#reload(sys)
#sys.setdefaultencoding("utf-8")


def createtraindata():
	""" Creates the traindata for the NER Tagger """
	newsHandler = codecs.open('test.set','r')
	#trainData = open('traindata_all.tsv', 'a')
	testData = open('testdata.tsv', 'w')
	newsList = []
	for line in newsHandler:
		newsList.append(line)
	#trainSplit = int(0.8 * len(newsList))
	#trainPart = newsList[:trainSplit]
	#testPart = newsList[trainSplit:]
	#createfiles(trainPart,trainData)
	#createfiles(testPart,testData)
	referenceDict = createfiles(newsList,testData)
	newsHandler.close()
	#trainData.close()
	testData.close()
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
		else:
			sentenceDict[str(lineList)] = [lineList]
	return sentenceDict

def tagdata(refDict):
	""" Gives the data its NER Tags using our trained tagger """
	#pbar = ProgressBar()
	tokens = []
	testData = codecs.open('testdata.tsv', 'r')
	for line in testData:
		if len(line) > 1:
			token = line.strip().split('\t')
			tokens.append(token[0])
	#os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
	path="ner"
	classifier = "ner-pta.ser.gz"
	jar = "stanford-ner.jar"
	tagger = NERTagger(classifier, jar)
	taggedText = tagger.tag(tokens)
	for line in taggedText:
		for tup in line:
			for key, value in refDict.items():
				if tup[0] == value[0]:
					refDict[key] = [tup[0],tup[1]]	
	return taggedText, refDict


def combineTags(sentence):
	""" Adds the tags to the testfile """
	#pbar = ProgressBar()
	refDict=defaultdict(list)
	sentList = []
	#for sentence in taggedText:
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
			refDict[i+1,words].append(newTuple)

		else: 
			newTuple = (words[0],words[1])
			sentList.append(newTuple)
			refDict[i+1,words].append(newTuple)

	for i, words in enumerate(sentList):
		if i != 0 and i < len(sentList)-1:
			sent=sentList[i-1][0],words[0],sentList[i+1][0]
			if words[1]!= 'O':
				mwords=words[0].replace(' ','_')
				if len(wn.synsets(mwords, 'n')) > 1:
					leskDec=lesk(word_tokenize(' '.join(sent)), mwords, 'n')
					for value in refDict.values():
						if value[0] == words and len(value) < 2:
							value.append([mwords,leskDec,leskDec.definition()])
				else:
					for ss in wn.synsets(mwords, 'n'):
						for value in refDict.values():
							if value[0] == words and len(value) < 2:
								value.append([mwords,ss, ss.definition()])
	return refDict
	
	
def updatedevset(referenceDict):
	""" Creates the file with NER tags """
	#pbar = ProgressBar()
	newsHandler = open('test.set','r')
	taggedHandler = open('nertagged.set','w')
	for line in newsHandler:
		lineList = line.strip().split()
		for key, value in referenceDict.items():
			if key == str(lineList):
				if len(value) > 1:
					if len(lineList) == 8:
						lineList.pop()
						lineList.pop()
					elif len(lineList) == 7:
						lineList.pop()
					lineList.append(value[1])
					taggedHandler.write(' '.join(lineList))
					taggedHandler.write('\n')
				else:
					taggedHandler.write(' '.join(lineList))
					taggedHandler.write('\n')
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
		elif len(lineItems) > 3:
			wordList.append((lineItems[4],'O'))
		else:
			wordList.append(('Empty', 'O'))
	taggedHandler.close()
	#print([word for word in wordList])
	return wordList

def getwikiurls(refDict):
	""" Searches for the wikipedia links """
	pbar = ProgressBar()
	wikiDict={}
	for key, value in pbar(refDict.items()):
		if value[0][1] != 'O' or value[0][1] != '-':
			if len(value) > 1:
				wikiresults = urllib.request.urlopen("http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+value[1][0]+"&format=json").readall().decode('utf-8')
				wikisuggs = json.loads(wikiresults)
				for query in wikisuggs:
					for search in wikisuggs[query]:
						if search == "search":
							decisionList=[]
							for article in wikisuggs[query][search]:
								if "snippet" in article:
									x=0
									for sent in article['snippet'].split():
										for word in sent:
											if str(word) in str(value[1][2]):
												x+=1
									decisionList.append((x, article.values()))
							if decisionList != []:
								for decision in decisionList:
									bestGuess = decisionList[0]
									newList=[]
									for item in list(bestGuess[1]):
										if type(item) == str:
											if item[0] != any(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']) and item[-1] != 'Z':
												newList.append(item)
										
									wikiLink= "http://en.wikipedia.org/wiki/"+sorted(newList, key=len)[0].replace(" ","_")
									#print(wikiLink)
									wikiDict[key] = wikiLink
									#print(wikiDict)
	
	return wikiDict

def addurls():#urls):
	""" Adds the wikipedia links to the file """
	urls = pickle.load(open('wikiurls.pickle','rb'))
	taggedHandler = open('nertagged.set','r')
	wikifiedHandler = open('wikitagged.set','w')

	for i, line in enumerate(taggedHandler):
		lineList=line.strip().split()
		if len(lineList) > 6 and (i+1,(lineList[4],lineList[6])) in urls.keys() :
			print("hoi")

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
		if len(line) < 7 :
			experiment.write(' '.join(line))
			experiment.write('\n')
		elif len(line) > 7:
			experiment.write(' '.join(line))
			experiment.write('\n')
			prevTag = line[6]
			prevWiki = line[7]
		elif len(line) == 7 and line[-1] != 'O':
			if line[6] == prevTag:
				line.append(prevWiki)
			else:
				link = 'http://en.wikipedia.org/wiki/'+line[4]+',1'
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


if __name__ == '__main__':
	#referenceDict = createtraindata()
	#os.popen("java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop")
	#taggedText, referenceDict = tagdata(referenceDict)
	#updatedevset(referenceDict)
	#taggedText = listtags()
	#decidedSs = combineTags(taggedText)
	#urls = getwikiurls(decidedSs)
	#print(urls)
	#with open('wikiurls.pickle','wb') as f:
	#	pickle.dump(urls,f)
	addurls()#urls)
	wikiexpander()
	reverseTagset()