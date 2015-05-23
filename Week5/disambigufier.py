import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	for value in wikiDict.values():
		value=re.sub(r'\[[0-9]*\]',"",value)
		text=sent_tokenize(value)
		for sent in word_tokenize(text):
			pos=pos_tag(sent)
			for i,word in enumerate(sent):
				if pos[i][1]=='NNPS' or pos[i][1]=='NNP' or pos[i][1]=='NNS' or pos[i][1]=='NN':
					if len(wn,synsets(word))>1: # TESTEN OF DEZE IF BIJ ALLE OR'S HIERBOVEN KAN ALS AND
						print(lesk(sent,word,pos[i]))

if __name__ == '__main__':
	main()