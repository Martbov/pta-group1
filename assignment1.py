#!usr/bin/python2.7

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
	#print("Answer to A: There are {} character types in the book, namely: {}".format(len(fDistChars),sorted(fDistChars)))
	#print("Answer to B: There are {} word types in the book, namely: {}".format(len(fDistWords),sorted(fDistWords)))
	#print("Answer to C: The 20 most common unigram characters are: \n")
	unigramList = []
	for u,f in fDistChars.items():
			unigramList.append((u,f))
	#print(unigramList[:20])
	print(fDistChars.most_common(20))


if __name__ == '__main__':
	main()
