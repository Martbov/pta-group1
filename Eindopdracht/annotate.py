# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter
from progressbar import ProgressBar
import os

def createtraindata():
	newsHandler = open('development.set','r')
	trainData = open('traindata.tsv', 'a')
	testData = open('testdata.tsv', 'a')
	newsList = []
	for line in newsHandler:
		newsList.append(line)
	trainSplit = int(0.8 * len(newsList))
	trainPart = newsList[:trainSplit]
	testPart = newsList[trainSplit:]
	createfiles(trainPart,trainData)
	createfiles(testPart,testData)
	newsHandler.close()
	trainData.close()
	testData.close()
	

def createfiles(Part,filename):
	pbar = ProgressBar()
	docId = ''
	for line in pbar(Part):
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			if docId != lineList[0]:
				filename.write('\n')
				filename.write(lineList[4]+'\t'+lineList[6]+'\n')
				docId = lineList[0]		
			else:
				filename.write(lineList[4]+'\t'+lineList[6]+'\n')
		elif len(lineList) > 5: 
			if docId != lineList[0]:
				filename.write('\n')
				filename.write(lineList[4]+'\t'+'O'+'\n')
				docId = lineList[0]		
			else:
				filename.write(lineList[4]+'\t'+'O'+'\n')

	"""for line in pbar(testPart):
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			if docId != lineList[0]:
				testData.append('\n')
				testData.append(lineList[4]+'\t'+lineList[6]+'\n')
				docId = lineList[0]		
			else:
				testData.append(lineList[4]+'\t'+lineList[6]+'\n')
		elif len(lineList) > 5: 
			if docId != lineList[0]:
				testData.append('\n')
				testData.append(lineList[4]+'\t'+'O'+'\n')
				docId = lineList[0]		
			else:
				testData.append(lineList[4]+'\t'+'O'+'\n')"""

	

def tagdata(tokens):
	os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
	path="ner"
	classifier = "ner-pta.ser.gz"
	jar = "stanford-ner.jar"
	tagger = NERTagger(classifier, jar)
	taggedText = tagger.tag(tokens)
	print(taggedText)



			

if __name__ == '__main__':
	text = createtraindata()
	os.popen("java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop")
	tagdata(text)


