import os, pickle
#from posopener import *

def getwikis():
	rootDir = "group1/"
	wikiList=[]
	for subdirs, dirs, files in os.walk(rootDir):
		if len(files) > 5:
			textFile = open(subdirs+"/"+files[5], 'r')
			print(textFile)
			rawText = textFile.readlines()
			for token in rawText:
				tokenspecs = token.split()
				if len(tokenspecs) == 7:
					wikiList.append(tokenspecs[6])
	return wikiList

def getText(wiki):
	os.system("curl '{}'| grep '<p>' | sed 's/<[^<]*>//g' > wiki.tmp".format(wiki))
	with open("wiki.tmp","r") as f:
		os.system("rm wiki.tmp")
		return f.read()

def main():
	wikiDict = {}
	wikis = getwikis()
	print(wikis)
	for wiki in set(wikis):
		print(wiki)
		text = getText(wiki)
		wikiDict[wiki] = text

	with open('wikis.pickle','wb') as f:
		pickle.dump(wikiDict,f,protocol=0)

if __name__ == '__main__':
	main()