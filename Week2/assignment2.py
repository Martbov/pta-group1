#!usr/bin/python3.4
import nltk
from collections import Counter
from nltk.tag.stanford import NERTagger
from nltk.corpus import wordnet as wn
import os
import codecs
from assignment1 import *

def main():
	os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
	path="C:\Users\Olivier\Copy\Premaster Information Science\PTA\pta-group1\Week2\stanford-ner-2014-06-16"
	classifier = path + "/classifiers/" + "english.muc.7class.distsim.crf.ser.gz"
	jar = path + "/stanford-ner-3.4.jar"
	tagger = NERTagger(classifier, jar)

	tokens=tokenize('ada_lovelace.txt')

	#taggedText = tagger.tag(tokens)

	countList=[]
	for taggedSent in taggedText:
		for taggedWord in taggedSent:
			countList.append(taggedWord[1])
			print(taggedWord)
	#print("Answer to 2.1: \n{} \nThey certainly aren't all correct.".format(Counter(countList)))
	#print()
	#print("Answer to 2.2: The other classifiers seem to achieve similar results,\nbut because of the multiple categories it is more interesting to read.")




if __name__ == '__main__':
	main()