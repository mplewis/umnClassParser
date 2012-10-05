#!/usr/bin/python3

# This short script breaks up a UMN course search URL into its arguments for inspection.

searchUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=CSCI%7CComputer+Science+-+CSCI&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"
rawSearchArgs = searchUrl.partition("http://onestop2.umn.edu/courseinfo/viewSearchResults.do?")[2]
rawSearchArgsSplit = rawSearchArgs.split('&')

searchArgs = []
for arg in rawSearchArgsSplit:
	arg = arg.split('=')
	searchArgs.append(arg)

for argTuple in searchArgs:
	print(argTuple[0] + ":", argTuple[1])