#!/usr/bin/python3

import urllib
from HTMLParser import HTMLParser

webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=ACCT%7CAccounting+-+ACCT&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"

courseCount = 0
insideCourseTitle = False

currCourseData = []
courseList = []

# create a subclass and override the handler methods
class ClassParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		# print "Encountered a start tag:", tag
		for attr in attrs:
			if attr[0] == "class" and attr[1] == "courseTitle":
				global courseCount, insideCourseTitle, currCourseData
				courseCount += 1
				insideCourseTitle = True
	def handle_endtag(self, tag):
		global insideCourseTitle
		if insideCourseTitle and tag == "h3":
			global currCourseData, courseList
			insideCourseTitle = False
			courseList.append(currCourseData)
			print currCourseData
			currCourseData = []
	def handle_data(self, data):
		global insideCourseTitle
		if insideCourseTitle:			
			currCourseData.append(data)

# instantiate the parser and fed it some HTML
parser = ClassParser()
parser.feed(urllib.urlopen(webUrl).read())

print "Courses found: ", courseCount
print courseList