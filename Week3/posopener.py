# 4 is Mart, 5 is Olivier

import os

def posopener(filenumber,exercise):
	rootDir = "group1/"
	posannoList=[]
	for subdirs, dirs, files in os.walk(rootDir):
		if len(files) > 5:
			textFile = open(subdirs+"/"+files[filenumber], 'r')
			rawText = textFile.readlines()
			for token in rawText:
				tokenspecs=token.split()
				if exercise == 3.1:
					try:
						tokenspecs[5]="annotated"
					except:
						pass
					posannoList.append(' '.join(tokenspecs[4:6]))
				else:
					posannoList.append(' '.join(tokenspecs[4:6]))
	return posannoList


#if __name__ == '__main__':
#	posopener(4,3.1)
