from collections import Counter
from nltk.metrics import ConfusionMatrix

import os

def posopener(tag,column):
	refList = []
	tagList = []
	cmref = []
	cmtag = []
	referenceFile = open('test.set', 'r')
	taggedFile = open('finalwiki.set', 'r')
	rawrefText = referenceFile.readlines()
	rawtagText = taggedFile.readlines()
	for token in rawrefText:
		tokenspecs=token.split()
		refList.append(token)
	for token in rawtagText:
		tokenspecs=token.split()
			#if tokenspecs[6] != 'O':
		tagList.append(token)
	for i, ref in enumerate(refList):
		refs=ref.strip().split()
		if len(refs) > column:
			cmref.append(refs[column])
			cmtag.append(tagList[i].strip().split()[column])
	#print(cmtag,cmref)

	return cmref, cmtag





def measurecalc(column, ref,tagged):
	cm = ConfusionMatrix(ref, tagged)

	print("Confusion Matrix for {}, Row= Reference, Column= Tagged \n{} ".format(column,cm))

	labels = set(tagged)

	true_positives = Counter()
	false_negatives = Counter()
	false_positives = Counter()

	for i in labels:
		for j in labels:
			if i == j:
				true_positives[i] += cm[i,j]
			else:
				false_negatives[i] += cm[i,j]
				false_positives[j] += cm[i,j]
	#print("Positives and negatives for exercise {} and their most common examples".format(exercise))
	print("TP:{} \nMost common are:{}".format(sum(true_positives.values()), true_positives.most_common()))
	print("FN:{} \nMost common are:{}".format(sum(false_negatives.values()), false_negatives.most_common()))
	print("FP:{} \nMost common are:{}".format(sum(false_positives.values()), false_positives.most_common()))
	print("\n")
	precision=recall=fscore=0 

	for i in sorted(labels):
		if true_positives[i] == 0:
			fscore = 0
		else:
			precision = true_positives[i] / (float(true_positives[i]+false_positives[i]))
			recall = true_positives[i] / (float(true_positives[i]+false_negatives[i]))
			fscore = 2 * ((precision * recall) / (float(precision + recall)))
		print("For class {}, precision= {}, recall= {} and Fscore = {}".format(i, precision, recall, fscore))
	totalprec=sum(true_positives.values())/(float(sum(true_positives.values())+sum(false_positives.values())))
	totalrec=sum(true_positives.values())/(float(sum(true_positives.values())+sum(false_negatives.values())))
	totalf= 2 * ((totalprec * totalrec) / (float(totalprec + totalrec)))

	print("\n")
	print("TOTAL FOR TAG {}: \nPrecision: {}\nRecall: {}\nFscore: {}".format(column,totalprec,totalrec,totalf))
	print("\n")

if __name__ == '__main__':
	
	nerref,nertagged = posopener("NERtags", 6)
	measurecalc("NERS",nerref,nertagged)
	wikiref,wikitagged = posopener("WIKIS", 7)
	measurecalc("WIKIS", nerref,nertagged)

