#!usr/bin/python3.4

import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
from collections import Counter

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	for value in wikiDict.values():
		value = re.sub(r'\[[0-9]*\]',"",value)
		text = sent_tokenize(value)
		print(text)

if __name__ == '__main__':
	main()