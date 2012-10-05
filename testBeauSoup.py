#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup

codeToUse = 'CSCI|Computer Science - CSCI'
courseNum = '1901'
webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=" + codeToUse + "&searchCatalogNumber=" + courseNum + "&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=false&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&searchLocations=TCEASTBANK%2CEast+Bank&searchLocations=TCWESTBANK%2CWest+Bank&searchLocations=STPAUL%2CSt.+Paul&campus=UMNTC&search=Search"

#rawWebData = str(urllib2.urlopen(webUrl).read())
with open('1902.html', 'r') as testFile:
	rawWebData = testFile.read()
parser = BeautifulSoup(rawWebData, "lxml")
for img in parser.find_all('img'):
	print img