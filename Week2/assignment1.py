#!usr/bin/python3.4

import nltk
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

def tokenize(textfile):
	textFile = open(textfile, 'r')
	rawText = textFile.read()
	textFile.close()
	sents = nltk.sent_tokenize(rawText)
	tokens = []
	for sent in sents:
		tokens += nltk.word_tokenize(sent)
	pos_tags = pos_tag(tokens)
	return tokens

def lemmatize(tokens):
	lemmatizer = WordNetLemmatizer()
	lemmatizer.lemmatize(lemma, wordnet.NOUN)