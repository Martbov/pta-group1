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
		most_common(bigramChars), most_common(trigramChars)))

	bigramWords = nltk.bigrams(tokens)
	trigramWords = nltk.trigrams(tokens)

	#print("Answer to 1D: The 20 most common words are: \nUnigrams: \n{}\nBigrams: \n{}\nTrigrams: \n{}".format(most_common(tokens), 
		most_common(bigramWords), most_common(trigramWords)))


	


if __name__ == '__main__':
	main()
