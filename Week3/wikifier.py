import os,pickle
from posopener import *

def getText(wiki):
	os.system("curl \"{}\"| grep \"<p>\" | sed \"s/<[^<]*>//g\" > wiki.tmp".format(wiki))
	with open("wiki.tmp","r") as f:
		os.system("rm wiki.tmp")
		return f.read()
wikiDict = {}
wikis = getwikis()
for wiki in set(wikis):
	print(wiki)
	text=getText(wiki)
	wikiDict[wiki]=text

with open('wikis.pickle','wb') as f:
		pickle.dump(wikiDict,f,protocol=0)


