import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
from collections import Counter

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	amountList = []
	for value in wikiDict.values():
		value = re.sub(r'\[[0-9]*\]',"",value)
		text = sent_tokenize(value)
		for sent in text:
			tokenized = word_tokenize(sent)
			pos = pos_tag(tokenized)
			for token, tag in pos:
				if (tag == 'NNPS' or tag == 'NNP' or tag == 'NNS' or tag == 'NN'):
					tag = "n"
					if len(wn.synsets(token, tag)) > 1:
						print(token, lesk(sent, token, tag))
						print("All possible senses:")
						n = 0
						for ss in wn.synsets(token, tag):
							print(ss, ss.definition())
							n += 1
						amountList.append(int(n))
						#print()
	#print(amountList)
	
	c2 = Counter(amountList)
	print(c2)
	

if __name__ == '__main__':
	main()