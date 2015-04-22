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
	#print(charList)
	fdist=nltk.FreqDist(charList)
	print("There are {} character types in the book".format(len(fdist)))
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	sorteD = sorted(bigram for bigram, score in scored)
	#print(tokens)

if __name__ == '__main__':
	main()
