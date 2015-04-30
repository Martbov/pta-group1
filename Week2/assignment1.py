#!usr/bin/python3.4

import nltk
import codecs
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn


def tokenize(textfile):
	textFile = codecs.open(textfile, 'r','utf-8')
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

def synsets(nounList):
	synsetList=[]
	for noun in nounList:
		synsetList.append(wn.synsets(noun))
	return synsetList
	
def hypernymOf(synset1, synset2):
	""" Returns True if synset2 is a hypernym of synset1, or if they are the same synset. Returns False otherwise. """
	if synset1 == synset2:
		return True
	for hypernym in synset1.hypernyms():
		if synset2 == hypernym:
			return True
		if hypernymOf(hypernym, synset2):
			return True
	return False


def main():
	infile = 'ada_lovelace.txt'
	tokens = tokenize(infile)
	nouns = lemmatize(tokens)
	synsetList = synsets(nouns)
	relativeSynsets = wn.synsets("relative", pos="n")
	illnessSynsets = wn.synsets("illness", pos="n")
	scienceSynsets = wn.synsets("science", pos="n")

	for synset in synsetList:
		#print(synset)
		hypernymOf(synset, relativeSynsets)
		hypernymOf(synset, illnessSynsets)
		hypernymOf(synset, scienceSynsets)


if __name__ == '__main__':
	main()