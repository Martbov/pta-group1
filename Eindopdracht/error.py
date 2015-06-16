newsHandler = open('test.set','r')
taggedHandler = open('nertagged.set','r')
taggedDict=[]
for line in taggedHandler:
	taggedDict.append(line.strip().split())

for line in newsHandler:
	lineList = line.strip().split()
	if lineList[:7] in taggedDict:
		print(lineList)