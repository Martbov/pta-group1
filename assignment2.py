#!usr/bin/python3.4

import nltk
from nltk.corpus import brown, treebank
from nltk.tag import UnigramTagger
from nltk import pos_tag
from collections import Counter

def main():
	brownDict={'.': 'sentence closer (. ; ? *)', '(': 'left paren', ')': 'right paren', '*': 'not, nt', '--': 'dash', ',': 'comma', ':': 'colon', 'ABL': 'pre-qualifier (quite, rather)', 'ABN': 'pre-quantifier (half, all)', 'ABX': 'pre-quantifier (both)', 'AP': 'post-determiner (many, several, next)', 'AT': 'article (a, the, no)', 'BE': 'be', 'BED': 'were', 'BEDZ': 'was', 'BEG': 'being', 'BEM': 'am', 'BEN': 'been', 'BER': 'are, art', 'BEZ': 'is', 'CC': 'coordinating conjunction (and, or)', 'CD': 'cardinal numeral (one, two, 2, etc.)', 'CS': 'subordinating conjunction (if, although)', 'DO': 'do', 'DOD': 'did', 'DOZ': 'does', 'DT': 'singular determiner/quantifier (this, that)', 'DTI': 'singular or plural determiner/quantifier (some, any)', 'DTS': 'plural determiner (these, those)', 'DTX': 'determiner/double conjunction (either)', 'EX': 'existential there', 'FW': 'foreign word (hyphenated before regular tag)', 'HV': 'have', 'HVD': 'had (past tense)', 'HVG': 'having', 'HVN': 'had (past participle)', 'IN': 'preposition', 'JJ': 'adjective', 'JJR': 'comparative adjective', 'JJS': 'semantically superlative adjective (chief, top)', 'JJT': 'morphologically superlative adjective (biggest)', 'MD': 'modal auxiliary (can, should, will)', 'NC': 'cited word (hyphenated after regular tag)', 'NN': 'singular or mass noun', 'NN$': 'possessive singular noun', 'NNS': 'plural noun', 'NNS$': 'possessive plural noun', 'NP': 'proper noun or part of name phrase', 'NP$': 'possessive proper noun', 'NPS': 'plural proper noun', 'NPS$': 'possessive plural proper noun', 'NR': 'adverbial noun (home, today, west)', 'OD': 'ordinal numeral (first, 2nd)', 'PN': 'nominal pronoun (everybody, nothing)', 'PN$': 'possessive nominal pronoun', 'PP$': 'possessive personal pronoun (my, our)', 'PP$$': 'second (nominal) possessive pronoun (mine, ours)', 'PPL': 'singular reflexive/intensive personal pronoun (myself)', 'PPLS': 'plural reflexive/intensive personal pronoun (ourselves)', 'PPO': 'objective personal pronoun (me, him, it, them)', 'PPS': '3rd. singular nominative pronoun (he, she, it, one)', 'PPSS': 'other nominative personal pronoun (I, we, they, you)', 'PRP': 'Personal pronoun', 'PRP$': 'Possessive pronoun', 'QL': 'qualifier (very, fairly)', 'QLP': 'post-qualifier (enough, indeed)', 'RB': 'adverb', 'RBR': 'comparative adverb', 'RBT': 'superlative adverb', 'RN': 'nominal adverb (here, then, indoors)', 'RP': 'adverb/particle (about, off, up)', 'TO': 'infinitive marker to', 'UH': 'interjection, exclamation', 'VB': 'verb, base form', 'VBD': 'verb, past tense', 'VBG': 'verb, present participle/gerund', 'VBN': 'verb, past participle', 'VBP': 'verb, non 3rd person, singular, present', 'VBZ': 'verb, 3rd. singular present', 'WDT': 'wh- determiner (what, which)', 'WP$': 'possessive wh- pronoun (whose)', 'WPO': 'objective wh- pronoun (whom, which, that)', 'WPS': 'nominative wh- pronoun (who, which, that)', 'WQL': 'wh- qualifier (how)', 'WRB': 'wh- adverb (how, where, when)'}

	sent = ['Marley', 'was', 'dead', ':', 'to', 'begin', 'with', '.', 'There', 'is', 'no', 'doubt', 'whatever', 'about', 'that', '.']
	
	# Part 1
	
	print("Brown tagger:")
	brownTagger = UnigramTagger(brown.tagged_sents())
	for word, tag in brownTagger.tag(sent):
		print(word,'->',tag)

	print("\nPENN Treebank Tagger:")
	pennTagger = UnigramTagger(treebank.tagged_sents())
	for word, tag in pennTagger.tag(sent):
		print(word, '->', tag)

	print("\nNLTK tagger:")
	nltkTagger = pos_tag(sent)
	for word, tag in nltkTagger:
		print(word, '->', tag)
		
	# Part 2

	br_tw = brown.tagged_words(categories='mystery')
	br_ts = brown.tagged_sents(categories='mystery')

	print("\nAnswer to 2A: \nWords: {} \nSentences: {}".format(len(br_tw), len(br_ts)))
	print("\nAnswer to 2B: \n100th word: {}, type is: {} \n101th word: {}, type is: {}".format(br_tw[99][0], brownDict.get(br_tw[99][1]), br_tw[100][0], brownDict.get(br_tw[100][1])))


	tagList=[]
	wordList=[]
	sentDict={}

	for sent in br_ts:
		for wordtag in sent:
			wordList.append(wordtag[0])
			tagList.append(brownDict.get(wordtag[1]))
			sentDict.setdefault(wordtag[1], [])
			sentDict[wordtag[1]].append(wordtag[0])


	print("\nAnswer to 2C: There are {} different tags being used.\n2D: 10 most common words are: \n{} \n2E: 10 most common tags are: \n {}".format(len(Counter(tagList)),Counter(wordList).most_common(10),Counter(tagList).most_common(10)))
	print("\nAnswer to 2F: Most common adverb (RB)= {} \n2G: Most common adjective (JJ)= {}".format(Counter(sentDict["RB"]).most_common(1),format(Counter(sentDict["JJ"]).most_common(1))))

	concDict={}
	tagTypes = []
	i=0
	tagTypesMeaning = []
	for word, tag in br_tw:
		concDict[i]=[i,str(tag),str(word)]
		i+=1
		if word == 'so':
			tagTypes.append(tag)
			tagTypesMeaning.append(brownDict.get(tag))
	tagTypesFreq = nltk.FreqDist(tagTypesMeaning)
	print("\nAnswer to 2H and 2I:\n{}".format(tagTypesFreq.most_common()))

	# 2k vanaf hier met CS QL RB:
	csplusList=[]
	csminList=[]
	qlplusList=[]
	qlminList=[]
	rbplusList=[]
	rbminList=[]
	csneighbourrightList=[]
	csneighbourleftList=[]
	qlneighbourrightList=[]
	qlneighbourleftList=[]
	rbneighbourrightList=[]
	rbneighbourleftList=[]
	for value in concDict.values():
		if value[2] == 'so' and value[1] == 'CS':
			csplusList.append(concDict.get(value[0]+1))
			csminList.append(concDict.get(value[0]-1))
		elif value[2] == 'so' and value[1] == 'QL':
			qlplusList.append(concDict.get(value[0]+1))
			qlminList.append(concDict.get(value[0]-1))
		elif value[2] == 'so' and value[1] == 'RB':
			rbplusList.append(concDict.get(value[0]+1))
			rbminList.append(concDict.get(value[0]-1))
	for item in csminList:
		csneighbourleftList.append(item[1])

	for item in csplusList:
		csneighbourrightList.append(item[1])

	for item in qlminList:
		qlneighbourleftList.append(item[1])

	for item in qlplusList:
		qlneighbourrightList.append(item[1])

	for item in rbminList:
		rbneighbourleftList.append(item[1])

	for item in rbplusList:
		rbneighbourrightList.append(item[1])

	uniqueList = []
	[uniqueList.append(tag) for tag in tagTypes if tag not in uniqueList]
	
	exampleList = []
	for sentence in br_ts:
		for word, tag in sentence:
			if word == 'so' and tag in uniqueList:
				sentenceStr = " ".join([w for w, t in sentence]) + "(" + brownDict.get(tag) + ")"
				exampleList.append(sentenceStr)
				uniqueList.remove(tag)

	print("\nAnswer to 2J:\n{}".format(exampleList))

	print("\nAnswer to 2K: \n Preceder of CS:{} \n Follower of CS: {}\n Preceder of QL: {}\n Follower of QL: {}\n Preceder of RB: {}\n Follower of RB: {}".format(brownDict.get(Counter(csneighbourleftList).most_common(1)[0][0]),brownDict.get(Counter(csneighbourrightList).most_common(1)[0][0]), brownDict.get(Counter(qlneighbourleftList).most_common(1)[0][0]), brownDict.get(Counter(qlneighbourrightList).most_common(1)[0][0]), brownDict.get(Counter(rbneighbourleftList).most_common(1)[0][0]), brownDict.get(Counter(rbneighbourrightList).most_common(1)[0][0])))
	
	# Part 3

	text = open('holmes.txt').read()[:500]
	tokens = nltk.wordpunct_tokenize(text)
	textTagged = pos_tag(tokens)
	print("\nPart 3, holmes.txt tokenized and POS-tagged:\n{}".format(textTagged))


if __name__ == '__main__':
	main()