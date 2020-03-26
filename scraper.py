from urllib import request as ureq
from collections import OrderedDict
import operator
import sys

class AppURLopener(ureq.FancyURLopener):
	version="Mozilla/5.0"

def parsed(x):
	symset = set()
	symset.add(',')
	symset.add('(')
	symset.add(')')
	symset.add('\"')
	symset.add('.')

	for y in x:
		if ((y >= 'a' and y <= 'z') or (y >= 'A' and y <= 'Z') or y in symset) == False:
			return x
	ret = ""
	for y in x:
		if y <= 'z' and y >= 'a':
			ret = ret + y
		elif y <= 'Z' and y >= 'A':
			ret = ret + chr(ord(y) + 32)
		elif not y in symset:
			ret = ret + y
	return ret

def main():
	argsList = list(sys.argv)
	argsList.pop(0)
	song_name = ""
	for x in argsList:
		song_name = song_name + x + '+'
	song_name = song_name + "lyrics" 
	my_url = "https://www.google.com/search?q=" + song_name
	opener = AppURLopener()
	response = opener.open(my_url)
	webpage = response.read().decode("utf-8")
	webpage = str(webpage)
	idx = webpage.find("class=\"hwc\"")
	cnt = 4
	useful = ""
	Dict = {}
	for i in range(idx,len(webpage)):
		if webpage[i] == '<' and cnt == 0:
			break;
		elif cnt == 0:
			useful = useful + webpage[i]
		if webpage[i] == '>':
			cnt = cnt - 1
	verses = [x for x in useful.split("\\n")]
	for x in verses:
		words = [parsed(y) for y in x.split()]
		for y in words:
			if y in Dict.keys():
				Dict[y] = Dict[y] + 1
			else:
				Dict[y] = 1
	
	sorted_Dict = dict(sorted(Dict.items(),key=operator.itemgetter(1),reverse=True))
	for key in sorted_Dict:
		print(key + " " + str(sorted_Dict[key]))
		pass

if __name__ == '__main__':
	main()
