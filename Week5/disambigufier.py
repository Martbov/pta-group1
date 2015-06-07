import pickle, nltk, re
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

def main():
	wikiDict = pickle.load(open('wikis.pickle','rb'))
	for value in wikiDict.values():
<<<<<<< HEAD
		value=re.sub(r'\[[0-9]*\]',"",value)
		text=sent_tokenize(value)
		for sent in word_tokenize(text):
			pos=pos_tag(sent)
			for i,word in enumerate(sent): # Misschien i en word omdraaien in deze loop, bij error
				if pos[i][1]=='NNPS' or pos[i][1]=='NNP' or pos[i][1]=='NNS' or pos[i][1]=='NN':
					if len(wn,synsets(word))>1: # TESTEN OF DEZE IF BIJ ALLE OR'S HIERBOVEN KAN ALS AND
						print(lesk(sent,word,pos[i]))
=======
		value = re.sub(r'\[[0-9]*\]',"",value)
		text = sent_tokenize(value)
		for sent in text:
			tokenized = word_tokenize(sent)
			pos = pos_tag(tokenized)
			#print(pos[1][1])
			for token, tag in pos:
				if pos[1][1] == 'NNPS' or pos[1][1] == 'NNP' or pos[1][1] == 'NNS' or pos[1][1] == 'NN':
					#print(sent, token, pos[1][1])
					leskoutput = lesk(sent, token, pos[1][1])
					if leskoutput != None:
						print(leskoutput)
				#if len(wn.synsets(word))>1: # TESTEN OF DEZE IF BIJ ALLE OR'S HIERBOVEN KAN ALS AND
				#	print(lesk(sent,word,pos[i]))
>>>>>>> 52b5b7861480788560b0acd57bd0432f7f93597d

if __name__ == '__main__':
	main()