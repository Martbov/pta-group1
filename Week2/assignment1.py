#!usr/bin/python3.4

import nltk
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

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

def synsets(nounList):
	relativeSynsets = wn.synsets("relative", pos="n")
	illnessSynsets = wn.synsets("illness", pos="n")
	scienceSynsets = wn.synsets("science", pos="n")
	synsetList=[]
	for noun in nounList:
		synsetList.append(wn.synsets('noun'))
	for synset in synsetList:
		print(synset[0].name())
	return synsetList


def main():
	infile = 'ada_lovelace.txt'
	tokens = tokenize(infile)
	nouns = lemmatize(tokens)
	synsets(nouns)

if __name__ == '__main__':
	main()