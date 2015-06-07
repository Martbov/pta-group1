# http://nlp.stanford.edu/software/crf-faq.shtml
# ner trainer call: java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop ptatagger.prop
from nltk.tag.stanford import NERTagger
from collections import Counter
import os

def createtraindata():
	newsHandler = open('development.set','r')
	trainData = open('traindata.tsv', 'a')
	testData = [] 
	for line in newsHandler:
		lineList = line.strip().split()
		if len(lineList) > 6 and len(lineList[6]) == 3:
			trainData.write(lineList[4]+'\t'+lineList[6]+'\n')
			testData.append(lineList[4])
	newsHandler.close()
	trainData.close()

	return testData

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


