#!/usr/bin/python

import urllib
from HTMLParser import HTMLParser

webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=ACCT%7CAccounting+-+ACCT&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"

# create a subclass and override the handler methods
class ClassParser(HTMLParser):
	def __init__(self):
		print "Initing ClassParser."
		self.insideCourseTitle = False
		self.currCourseData = []
		self.courseList = []
		print "Resetting HTMLParser."
		super(ClassParser, self).__init__()
	def handle_starttag(self, tag, attrs):
		for attr in attrs:
			if attr[0] == "class" and attr[1] == "courseTitle":
				self.insideCourseTitle = True
	def handle_endtag(self, tag):
		if insideCourseTitle and tag == "h3":
			self.insideCourseTitle = False
			self.courseList.append(currCourseData)
			print self.currCourseData
			self.currCourseData = []
	def handle_data(self, data):
		if self.insideCourseTitle:
			self.currCourseData.append(data)
	def getParsedData(self):
		return self.courseList

parser = ClassParser()

#print "Fetching data..."
#rawWebData = urllib.urlopen(webUrl).read()

rawFileData = open("./acctData.html", 'r')
parser.feed(rawFileData)


print "Courses found: ", courseCount
print courseList