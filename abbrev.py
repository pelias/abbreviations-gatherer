import BeautifulSoup
import urllib2
import json
import sys

def getParsedSite():
	try:
		rawdata = urllib2.urlopen("http://wiki.openstreetmap.org/wiki/Name_finder:Abbreviations")
		parsed = BeautifulSoup.BeautifulSoup(rawdata)
		return parsed
	except:
		print "Couldn't reach server. Check your internet connection"
		sys.exit()

def getLanguageTable(index):
	parsed = getParsedSite()
	return parsed.findAll("table")[index]

def listLanguages():
	parsed = getParsedSite()
	i = 0
	for header in parsed.findAll("h2"):
		if header.span and header.span.string != "Template for another language":
			span = header.span
			print i, "-", span.string
			i += 1

def parseLanguage(languageTable):
	abbreviationList = []
	for abbreviationElement in languageTable.findAll("tr")[1:]:
		abbreviationList.append(parseRow(abbreviationElement))
	return abbreviationList

def parseRow(rowElement):
	assert len(rowElement.findAll("td")) == 6
	keys = ["fullword", "abbreviation", "concatenated", "separable", "implemented", "notes"]
	rowDic = dict.fromkeys(keys)
	tds = rowElement.findAll("td")
	rowDic["fullword"] = tds[0].text
	rowDic["abbreviation"] = tds[1].text
	rowDic["concatenated"] = True if tds[2].text != 'no' else False
	rowDic["separable"] = tds[3].text
	rowDic["implemented"] = True if tds[2].text != 'no' else False
	rowDic["notes"] = tds[5].text
	return rowDic

def toJSON(dict):
	return json.dumps(dict)

def export(jsonFile):
	file = open("file.json", "w")
	file.write(jsonFile)


def ex(index):
	languageTable = getLanguageTable(index)
	languageData = parseLanguage(languageTable)
	jsonData = toJSON(languageData)
	export(jsonData)


if "-l" in sys.argv:
	listLanguages()

elif "-g" in sys.argv:
	index = sys.argv.index("-g")+1
	
	if sys.argv[index].isdigit():
		ex(index)

	elif sys.argv[index] == "-all":
		pass

	else:
		print "You need to specify one of the following indices or add --all"
		listLanguages()

else:
	print "You need to specify an option"
