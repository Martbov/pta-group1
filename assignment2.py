#!usr/bin/python2.7

from nltk.corpus import brown, treebank
from nltk.tag import UnigramTagger
from nltk import pos_tag

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

	



if __name__ == '__main__':
	main()