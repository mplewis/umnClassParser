#!/usr/bin/python3

import urllib.request
from html.parser import HTMLParser

'''ACCT classes'''
#webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=ACCT%7CAccounting+-+ACCT&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"
'''BIOL classes'''
#webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=BIOL%7CBiology+-+BIOL&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"
'''CSCI classes'''
webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=CSCI%7CComputer+Science+-+CSCI&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"

# create a subclass and override the handler methods
class CourseParser(HTMLParser):
	def __init__(self):
		# must init HTMLParser with strict = false, or else bad tags will break parser
		super().__init__(strict = False)
		# if insideCourseTitle is true, then the script is reading a course title and should keep track of the data
		# insideCourseTitle is true after <h3 class="courseTitle"> and before </h3>
		self.insideCourseTitle = False
		# currCourseData holds data about each course
		# currently only pulls data in between <h3> </h3> tags
		# appends list [course 4-letter category code (HIST, CSCI, etc), course number, course title]
		#     to end of courseList
		self.currCourseData = []
		# courseList is a list of currCourseData items, one per course
		self.courseList = []
	def handle_starttag(self, tag, attrs):
		for attr in attrs:
			if attr[0] == "class" and attr[1] == "courseTitle":
				self.insideCourseTitle = True
	def handle_endtag(self, tag):
		if self.insideCourseTitle and tag == "h3":
			self.insideCourseTitle = False
			self.courseList.append(self.currCourseData)
			self.currCourseData = []
	def handle_data(self, data):
		if self.insideCourseTitle:
			self.currCourseData.append(data)
	def getCourseList(self):
		return self.courseList

parser = CourseParser()

print("Fetching data...")
rawWebData = str(urllib.request.urlopen(webUrl).read())
parser.feed(rawWebData)

#rawFileData = open("./acctData.html", 'r')
#parser.feed(rawFileData)

#parser.feed('<html><head><title>Test</title></head><body><h3 class="courseTitle">Parse me!</h3></body></html>')

courseList = parser.getCourseList()

for course in courseList:
	print("Course:", course[0], course[1])
	print("\t", course[2])

print(len(courseList), "courses found.")