#!usr/bin/python3.4

import nltk
from nltk.collocations import *


def most_common(countList):
	listFreq = nltk.FreqDist(countList)
	return listFreq.most_common(20)

def main():
	text = open('holmes.txt').read()
	tokens = nltk.wordpunct_tokenize(text)
	charList = []
	for word in tokens:
		for char in word:
			charList.append(char)
	fDistChars = nltk.FreqDist(charList)
	fDistWords = nltk.FreqDist(tokens)
	#print("Answer to 1A: There are {} character types in the book, namely: {}".format(len(fDistChars),sorted(fDistChars)))
	#print("Answer to 1B: There are {} word types in the book, namely: {}".format(len(fDistWords),sorted(fDistWords)))
	bigramChars = nltk.bigrams(charList)
	trigramChars = nltk.trigrams(charList)

	#print("Answer to 1C: The 20 most common characters are: \nUnigrams: \n{}\nBigrams: \n{}\nTrigrams: \n{}".format(most_common(charList), 
		#most_common(bigramChars), most_common(trigramChars)))

	bigramWords = nltk.bigrams(tokens)
	trigramWords = nltk.trigrams(tokens)

	#print("Answer to 1D: The 20 most common words are: \nUnigrams: \n{}\nBigrams: \n{}\nTrigrams: \n{}".format(most_common(tokens), 
		#most_common(bigramWords), most_common(trigramWords)))
	
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokens)
	scoredPMI = finder.score_ngrams(bigram_measures.pmi)
	scoredCHI = finder.score_ngrams(bigram_measures.chi_sq)
	#print("Answer to 2: The 20 most likely collocations are:\n PMI:\n {} \n Chi's square\n {}" .format(scoredPMI[:20],scoredCHI[:20]))
	
	print("Spearmans correlation = {}".format(nltk.metrics.spearman.spearman_correlation(scoredPMI, scoredCHI)))

if __name__ == '__main__':
	main()
