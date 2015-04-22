#!usr/bin/python2.7

from nltk.corpus import brown 
from nltk.tag import UnigramTagger
	
tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
sent = ['Marley', 'was', 'dead', ':', 'to', 'begin', 'with', '.', 'There', 'is', 'no', 'doubt', 'whatever', 'about', 'that', '.']
for word, tag in tagger.tag(sent):
	print(word,'->',tag)


