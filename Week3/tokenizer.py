#!usr/bin/python3.4

import sys
import nltk
from nltk import pos_tag
import os

def main():
	rootDir = "group1/"
	for subdirs, dirs, files in os.walk(rootDir):
		if len(files) == 3:
			textFile = open(subdirs+"/"+files[2], 'r')
			rawText = textFile.readlines()
			tokenList = []
			originalList = []
			for sent in rawText:
				begin,eind,idee,token = sent.strip().split()
				originalList.append([begin,eind,idee,token])
				tokenList.append(token)
				pos_tags = pos_tag(tokenList)
			x=0	
			textFile1 = open(subdirs+"/"+files[2]+'.pos', 'a')
			textFile2 = open(subdirs+"/"+files[2]+'.pos_olivier', 'a')
			textFile3 = open(subdirs+"/"+files[2]+'.pos_mart', 'a')

			for item in originalList:
				item.append(pos_tags[x][1])
				x+=1
				newLine = ' '.join(item)+"\n"
				textFile1.write(newLine)
				textFile2.write(newLine)
				textFile3.write(newLine)
			textFile1.close()
			textFile2.close()
			textFile3.close()

				
			



if __name__ == '__main__':
	main()