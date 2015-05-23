import os
from posopener import *

def getText(wiki):
    os.system("curl '{0}' | grep '<p>' | sed 's/<[^<]*>//g' > wiki.tmp".format(wiki))
    with open("wiki.tmp","r") as f:
        os.system("rm wiki.tmp")
        return f.read()

wikiDict = {}
wikis = getwikis()
for wiki in set(wikis):
	text=getText(wiki)
	wikiDict[wiki]=text

 
print wikiDict