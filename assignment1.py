#!usr/bin/python3.4

import nltk
from nltk.collocations import *

def main():
	text = open('holmes.txt').read()
	tokens = nltk.wordpunct_tokenize(text)
	charList = []
	for word in tokens:
		for char in word:
			charList.append(char)
	fDistChars = nltk.FreqDist(charList)
	fDistWords = nltk.FreqDist(tokens)
	print("Answer to A: There are {} character types in the book, namely: {}".format(len(fDistChars),sorted(fDistChars)))
	print("Answer to B: There are {} word types in the book, namely: {}".format(len(fDistWords),sorted(fDistWords)))
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	sorteD = sorted(bigram for bigram, score in scored)

if __name__ == '__main__':
	main()
