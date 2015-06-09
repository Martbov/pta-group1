# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter
import os

def createtraindata():
	newsHandler = open('development.set','r')
	trainData = open('traindata.tsv', 'a')
	testData = []
	newsList = []
	for line in newsHandler:
		newsList.append(line)
	trainSplit = int(0.8 * len(newsList))
	trainPart = newsList[:trainSplit]
	testPart = newsList[trainSplit:]
	docId = ''
	for i, line in enumerate(trainPart):
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			if docId != lineList[0]:
				trainData.write('\n')
				trainData.write(lineList[4]+'\t'+lineList[6]+'\n')
				docId = lineList[0]		
			else:
				trainData.write(lineList[4]+'\t'+lineList[6]+'\n')
	for line in testPart:
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			testData.append(lineList[4])
	newsHandler.close()
	trainData.close()

	return testData

def tagdata(tokens):
	#os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
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


