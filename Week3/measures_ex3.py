# Call: python2 measures_ex3.py
from collections import Counter
from nltk.metrics import ConfusionMatrix
from posopener import *

def measurecalc(ref,tagged,exercise):
	cm = ConfusionMatrix(ref, tagged)

	print("Confusion Matrix for exercise {}, Row= Mart, Column= Olivier \n{} ".format(exercise,cm))

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
	print("Positives and negatives for exercise {} and their most common examples".format(exercise))
	print("TP:{} \nMost common are:{}".format(sum(true_positives.values()), true_positives.most_common()))
	print("FN:{} \nMost common are:{}".format(sum(false_negatives.values()), false_negatives.most_common()))
	print("FP:{} \nMost common are:{}".format(sum(false_positives.values()), false_positives.most_common()))
	print("\n") 

	for i in sorted(labels):
		if true_positives[i] == 0:
			fscore = 0
		else:
			precision = true_positives[i] / float(true_positives[i]+false_positives[i])
			recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
			fscore = 2 * (precision * recall) / float(precision + recall)
		print("For class {}, precision= {}, recall= {} and Fscore = {}".format(i, precision, recall, fscore))
	totalprec=sum(true_positives.values())/float(sum(true_positives.values())+sum(false_positives.values()))
	totalrec=sum(true_positives.values())/float(sum(true_positives.values())+sum(false_negatives.values()))
	totalf= 2 * (totalprec * totalrec) / float(totalprec + totalrec)

	print("\n")
	print("TOTAL FOR EXERCISE {}: \nPrecision: {}\nRecall: {}\nFscore: {}".format(exercise,totalprec,totalrec,totalf))
	print("\n")

if __name__ == '__main__':
	posopener(4,3.1)
	posannoMart = posopener(4,3.1)
	posannoOlivier = posopener(5,3.1)
	measurecalc(posannoMart,posannoOlivier,3.1)

	raw_input("Press Enter to see the results of exercise 3.2.")
	posannoMart = posopener(4,3.2)
	posannoOlivier = posopener(5,3.2)
	measurecalc(posannoMart,posannoOlivier,3.2)

