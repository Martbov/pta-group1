#!usr/bin/python3.4
import nltk
from collections import Counter
from nltk.tag.stanford import NERTagger
from nltk.corpus import wordnet as wn
import os
import codecs
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

def tokenize(textfile):
	textFile = open(textfile, 'r')
	rawText = textFile.read()
	textFile.close()
	sents = nltk.sent_tokenize(rawText)
	tokens = []
	nounTokens = []
	for sent in sents:
		tokens += nltk.word_tokenize(sent)
		pos_tags = pos_tag(tokens)
		for token in pos_tags:
			if token[1] == 'NN' or token[1] == 'NNP' or token[1] == 'NNS' or token[1] == 'NNPS':
				nounTokens.append(token[0])
	return nounTokens

def lemmatize(tokens):
	lemmatizer = WordNetLemmatizer()
	nounLemmas = []
	for token in tokens:
		nounLemmas.append(lemmatizer.lemmatize(token, wn.NOUN))
	return nounLemmas

def main():
	#os.environ['JAVAHOME'] = "C:\Program Files\Java\jdk1.8.0_45/bin"
	path="ner"
	classifier = path + "/classifiers/" + "english.muc.7class.distsim.crf.ser.gz"
	jar = path + "/stanford-ner-3.4.jar"
	tagger = NERTagger(classifier, jar)

	tokens = tokenize('ada_lovelace.txt')
	#print(tokens)

	taggedText = tagger.tag(tokens)
	

	countList=[]
	nounList = []
	for word, tag in taggedText:
		if tag != 'O':
			countList.append(tag)
			nounList.append(word)

	
	#print("Answer to 2.1: \n{} \nThey certainly aren't all correct.".format(Counter(countList)))
	#print()
	#print("Answer to 2.2: The other classifiers seem to achieve similar results,\nbut because of the multiple categories it is more interesting to read.")

	lemmas = lemmatize(nounList)
	print(lemmas)



if __name__ == '__main__':
	main()