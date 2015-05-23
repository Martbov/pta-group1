import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	for value in wikiDict.values():
		value=re.sub(r'\[[0-9]*\]',"",value)
		text=sent_tokenize(value)
		for sent in word_tokenize(text):
			pos=pos_tag(sent)
			for i,word in enumerate(sent):
				print(lesk(sent,word,pos[i]))



		tokens = [word for sent in sent_tokenize(value) for word in word_tokenize(sent)]

if __name__ == '__main__':
	main()