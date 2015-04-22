#!usr/bin/python3.4

import nltk
from nltk.collocations import *

def main():
	text = open('holmes.txt').read()
	tokens = nltk.wordpunct_tokenize(text)
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	sorteD = sorted(bigram for bigram, score in scored)
	print(sorteD)

if __name__ == '__main__':
	main()