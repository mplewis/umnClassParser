# this script is specifically meant to extract categories from courseCats.html
# the category list it produces is saved in catList.txt

from html.parser import HTMLParser

class CatParser(HTMLParser):
	def __init__(self):
		super().__init__(strict = False)
		self.catList = []
		#self.insideTag = False
	def handle_starttag(self, tag, attrs):
		self.catList.append(attrs[0][1])
		#self.insideTag = True
	#def handle_endtag(self, tag):
		#self.insideTag = False
	#def handle_data(self, data):
		#if (self.insideTag):
		#	print(data)
	def getCatList(self):
		return self.catList

parser = CatParser()

catFile = open("./courseCats.html", 'r')
strFile = str(catFile.read())

parser.feed(strFile)

catList = parser.getCatList()

print(catList)
#print("Categories found: ", len(catList))