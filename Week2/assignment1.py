#!usr/bin/python3.4

import nltk
import codecs
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import Counter, defaultdict


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

def makeSynsets(nounList):
	synsetList=[]
	for noun in nounList:
		synsetList.append((noun, wn.synsets(noun)))
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

def getHypernyms(synset, noun, top25):
	for hypernym in synset.hypernyms():
		for key in top25:
			if hypernym.name().split('.')[0] in key:
				top25[key].append(noun)
				break
		if hypernym.name() == 'entities':
			return words
		else:
			getHypernyms(hypernym, noun, top25)

def main():
	infile = 'ada_lovelace.txt'
	tokens = tokenize(infile)
	nouns = lemmatize(tokens)
	synsetList = makeSynsets(nouns)
	relativeSynsets = wn.synsets("relative", pos="n")
	illnessSynsets = wn.synsets("illness", pos="n")
	scienceSynsets = wn.synsets("science", pos="n")
	
	
	
	relativeNouns = []
	illnessNouns = []
	scienceNouns = []
	for lemma, synsets in synsetList:
		for synset in synsets:
			for relativesyn in relativeSynsets:
				if hypernymOf(synset, relativesyn) == True:
					relativeNouns.append(lemma)
			for illnesssyn in illnessSynsets:
				if hypernymOf(synset, illnesssyn) == True:
					illnessNouns.append(lemma)
			for sciencesyn in scienceSynsets:
				if hypernymOf(synset, sciencesyn) == True:
					scienceNouns.append(lemma)
	countRelative = Counter(relativeNouns)
	countIllness = Counter(illnessNouns)
	countScience = Counter(scienceNouns)
	#print(countRelative, countIllness, countScience)

	categories = ['act,action,activity', 'animal,fauna', 'artifact', 'attribute,property', 'body,corpus', 'cognition,knowledge', 'communication', 'event,happening', 'feeling,emotion', 'food', 'group,collection', 'location,place', 'motive', 'plant,flora', 'possession', 'process', 'quantity,amount', 'relation', 'shape', 'state,condition', 'substance', 'time']
	top25 = defaultdict(list)
	for category in categories:
		key = category.split(',')
		top25[tuple(key)] = []

	for lemma, synsets in synsetList:
		for synset in synsets:
			words = getHypernyms(synset, lemma, top25)
	totallen=0
	for lists in top25.values():
		totallen+=len(Counter(lists))
	print(totallen /22)
		

if __name__ == '__main__':
	main()