import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	for value in wikiDict.values():
		value = re.sub(r'\[[0-9]*\]',"",value)
		text = sent_tokenize(value)
		for sent in text:
			tokenized = word_tokenize(sent)
			pos = pos_tag(tokenized)
			for token, tag in pos:
				if tag == 'NNPS' or tag == 'NNP' or tag == 'NNS' or tag == 'NN':
					tag = "n"
					if len(wn.synsets(token))>1: # TESTEN OF DEZE IF BIJ ALLE OR'S HIERBOVEN KAN ALS AND
						print(lesk(sent, token, tag))

if __name__ == '__main__':
	main()