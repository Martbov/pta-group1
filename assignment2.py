#!usr/bin/python2.7
import nltk
from nltk.corpus import brown, treebank
from nltk.tag import UnigramTagger
from nltk import pos_tag
from collections import Counter

def main():
	sent = ['Marley', 'was', 'dead', ':', 'to', 'begin', 'with', '.', 'There', 'is', 'no', 'doubt', 'whatever', 'about', 'that', '.']

	# Deel 1
	"""print("Brown tagger:")
	brownTagger = UnigramTagger(brown.tagged_sents())
	for word, tag in brownTagger.tag(sent):
		print(word,'->',tag)

	print("PENN Treebank Tagger:")
	pennTagger = UnigramTagger(treebank.tagged_sents())
	for word, tag in pennTagger.tag(sent):
		print(word, '->', tag)

	print("NLTK tagger:")
	print(pos_tag(sent))"""

	# Deel 2

	br_tw = brown.tagged_words(categories='mystery')
	br_ts = brown.tagged_sents(categories='mystery')

	#print("Answer to 2A: \nWords: {} \nSentences: {}".format(len(br_tw), len(br_ts)))
	#print("Answer to 2B: \n100th word: {} \n101th word: {}".format(br_tw[99][0], br_tw[100][0]))

	for word, tag in br_ts:
		print(type(word))

	
		



	#print("Answer to 2C: There are {} different tags being used.\n 2D: 10 most common words are: \n {} \n 2E: 10 most common tags are: \n {}".format(len(cTag),cWord.most_common(10),cTag.most_common(10)))
	
	
	
		

	"""brownTagger = UnigramTagger(brown.tagged_sents())
	for word, tag in brownTagger.tag(sent):
		print(word,'->',tag)"""



if __name__ == '__main__':
	main()
