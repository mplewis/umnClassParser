#!/usr/bin/python
# This script is now for Python 2

import urllib2
from HTMLParser import HTMLParser
import sys

if len(sys.argv) <= 1 or sys.argv[1] == "":
	sys.exit("No course code provided. Please provide a course code such as BIOL or CSCI.\n" + 
             "Use course code \"****\" to search all categories.")
else:
	argCourseCat = sys.argv[1]

if len(sys.argv) <= 2:
	argCourseNum = ""
else:
	argCourseNum = sys.argv[2]

class CourseParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.reset()

	def reset(self):
		HTMLParser.reset(self)
		self.courseList  = []
		self.courseData  = []
		self.courseInfo  = []
		self.sectionData = []
		self.sectionInfo = []
		self.seatsData   = []
		self.insideCourseTitle      = False
		self.insideSectionNumber    = False
		self.insideSeatsUnavailable = False
		self.insideSeatsAvailable   = False
		self.isFirstCourse = True
		self.courseCount  = 0
		self.sectionCount = 0

	def finalize(self):
		# consolidate all data into courseList before adding a new course
		self.courseData.append(self.sectionData)
		self.courseList.append(self.courseData)
		self.courseData  = []
		self.courseInfo  = []
		self.sectionData = []

	def handle_starttag(self, tag, attrs):
		for attr in attrs:
			if attr[0] == "class" and attr[1] == "courseTitle":
				# don't consolidate any data if this is the first course seen;
				#     there's no data to consolidate
				if self.isFirstCourse:
					self.isFirstCourse = False
				else:
					self.finalize()
				self.insideCourseTitle = True
			elif tag == "td" and attr[0] == "class" and attr[1] == "classNumber":
				self.insideSectionNumber = True
			elif tag == "span" and attr[0] == "class" and attr[1] == "closed":
				self.insideSeatsUnavailable = True
			elif tag == "img" and attr[0] == "alt" and attr[1] == "Seats Open":
				self.insideSeatsAvailable = True

	def handle_endtag(self, tag):
		if self.insideCourseTitle and tag == "h3":
			self.insideCourseTitle = False
			# converting course number to int doesn't work because of Honors
			#     courses (1001H, etc.) so don't do it!
			# consolidate courseInfo into courseData
			self.courseData.append(self.courseInfo)
			self.courseInfo = []
			self.courseCount += 1
		if self.insideSectionNumber and tag == "td":
			self.insideSectionNumber = False
			# don't consolidate yet; still need to add seats info
		if self.insideSeatsUnavailable and tag == "span":
			self.insideSeatsUnavailable = False
			# ONLY consolidate seatsData if a section exists; sometimes OneStop says
			#     "Closed" without providing a section number. This is bad.
			if len(self.sectionInfo) > 0:
				# consolidate seatsData (unavailable) into sectionInfo
				self.sectionInfo.append(-1) # available seats
				self.sectionInfo.append(-1) # total seats
				# consolidate sectionInfo into sectionData
				self.sectionData.append(self.sectionInfo)
				self.sectionInfo = []
				self.sectionCount += 1
		if self.insideSeatsAvailable and tag == "span":
			self.insideSeatsAvailable = False
			# ONLY consolidate seatsData if a section exists; sometimes OneStop says
			#     "Closed" without providing a section number. This is bad.
			if len(self.sectionInfo) > 0:
				# consolidate seatsData into sectionInfo, converting seats to ints
				self.sectionInfo.append(int(self.seatsData[0])) # available seats
				self.sectionInfo.append(int(self.seatsData[2])) # total seats
				self.seatsData = []
				# consolidate sectionInfo into sectionData
				self.sectionData.append(self.sectionInfo)
				self.sectionInfo = []
				self.sectionCount += 1

	def handle_data(self, data):
		if self.insideCourseTitle:
			self.courseInfo.append(data)
		if self.insideSectionNumber:
			#FIXME THIS IS SUPER HACKY AND SHOULD NEVER BE TRUSTED AND CAUSES BUGS
			try:
				self.sectionInfo.append(int(data))
			except ValueError:
				self.sectionInfo.append(-1)
		if self.insideSeatsAvailable:
			self.seatsData.append(data)

	def getCourseList(self):
		return self.courseList

	def getCourseCount(self):
		return self.courseCount

	def getSectionCount(self):
		return self.sectionCount

def getCourseSearchURL(courseCat, courseNum = ""):
	courseCodes = ['****|****', 'AHS|Academic Health Center Shared - AHS', 'ACCT|Accounting - ACCT', 'ADDS|Addiction Studies - ADDS', 'ADED|Adult Education - ADED', 'ADPY|Adult Psychiatry - ADPY', 'AEM|Aerospace Engineering and Mechanics - AEM', 'AIR|Aerospace Studies - AIR', 'AFRO|African American and African Studies - AFRO', 'AIM|Agricultural Industries and Marketing - AIM', 'AFEE|Agricultural, Food, and Environmental Education - AFEE', 'AGRO|Agronomy and Plant Genetics - AGRO', 'AMIN|American Indian Studies - AMIN', 'ASL|American Sign Language - ASL', 'AMST|American Studies - AMST', 'ANAT|Anatomy - ANAT', 'ANES|Anesthesiology - ANES', 'ANSC|Animal Science - ANSC', 'ANTH|Anthropology - ANTH', 'ADES|Apparel Design - ADES', 'APST|Apparel Studies - APST', 'ABUS|Applied Business - ABUS', 'APEC|Applied Economics - APEC', 'APSC|Applied Plant Sciences - APSC', 'APS|Applied Professional Studies - APS', 'ARAB|Arabic - ARAB', 'ARCH|Architecture - ARCH', 'ARTS|Art - ARTS', 'ARTH|Art History - ARTH', 'ACL|Arts and Cultural Leadership - ACL', 'AAS|Asian American Studies - AAS', 'ALL|Asian Languages and Literatures - ALL', 'AST|Astronomy - AST', 'BIOC|Biochemistry - BIOC', 'BTHX|Bioethics, Center for - BTHX', 'BINF|Bioinformatics - BINF', 'BIOL|Biology - BIOL', 'BSE|Biology, Society, and Environment - BSE', 'BMEN|Biomedical Engineering - BMEN', 'BPHY|Biophysical Sciences - BPHY', 'BBE|Bioproducts and Biosystems Engineering - BBE', 'BA|Business Administration - BA', 'BLAW|Business Law - BLAW', 'BIE|Business and Industry Education - BIE', 'CAHP|Center for Allied Health Programs - CAHP', 'CSPH|Center for Spirituality and Healing - CSPH', 'CHEN|Chemical Engineering - CHEN', 'CHPH|Chemical Physics - CHPH', 'CHEM|Chemistry - CHEM', 'CHIC|Chicano Studies - CHIC', 'CPSY|Child Psychology - CPSY', 'CAPY|Child and Adolescent Psychiatry - CAPY', 'CHN|Chinese - CHN', 'CE|Civil Engineering - CE', 'CLCV|Classical Civilization - CLCV', 'CNES|Classical and Near Eastern Studies - CNES', 'CLS|Clinical Laboratory Science - CLS', 'CLSP|Clinical Laboratory Sciences Program - CLSP', 'CPMS|Clinical Physiology and Movement Science - CPMS', 'CGSC|Cognitive Science - CGSC', 'CFAN|College of Food, Agri & Natural Resource Sciences - CFAN', 'CLA|College of Liberal Arts - CLA', 'CSE|College of Science and Engineering - CSE', 'COMM|Communication Studies - COMM', 'CL|Comparative Literature - CL', 'CSDS|Comparative Studies in Discourse and Society - CSDS', 'CMB|Comparative and Molecular Biosciences - CMB', 'CMPE|Computer Engineering - CMPE', 'CSCI|Computer Science - CSCI', 'CBIO|Conservation Biology - CBIO', 'CMGT|Construction Management - CMGT', 'CDED|Continuing Dental Education - CDED', 'CSDY|Control Science and Dynamical Systems - CSDY', 'CSCL|Cultural Studies and Comparative Literature - CSCL', 'CI|Curriculum and Instruction - CI', 'DAKO|Dakota - DAKO', 'DNCE|Dance - DNCE', 'DH|Dental Hygiene - DH', 'DT|Dental Therapy - DT', 'DENT|Dentistry - DENT', 'DERM|Dermatology - DERM', 'DES|Design - DES', 'DSSC|Development Studies and Social Change - DSSC', 'DDS|Doctor of Dental Surgery - DDS', 'DTCH|Dutch - DTCH', 'EMS|Early Modern Studies - EMS', 'ESCI|Earth Sciences - ESCI', 'EAS|East Asian Studies - EAS', 'EEB|Ecology, Evolution, and Behavior - EEB', 'ECON|Economics - ECON', 'EDUC|Education - EDUC', 'EDHD|Education and Human Development - EDHD', 'EDPA|Educational Policy and Administration - EDPA', 'EPSY|Educational Psychology - EPSY', 'EE|Electrical and Computer Engineering - EE', 'EMMD|Emergency Medicine - EMMD', 'ENDO|Endodontics - ENDO', 'ESL|English as a Second Language - ESL', 'ENGL|English:  Literature - ENGL', 'ENGW|English: Creative Writing - ENGW', 'ENT|Entomology - ENT', 'ENTR|Entrepreneurship - ENTR', 'ESPM|Environmental Sciences, Policy, and Management - ESPM', 'ECP|Experimental and Clinical Pharmacology - ECP', 'FMCH|Family Medicine and Community Health - FMCH', 'FSOS|Family Social Science - FSOS', 'FINA|Finance - FINA', 'FM|Financial Mathematics - FM', 'FIN|Finnish - FIN', 'FW|Fisheries and Wildlife - FW', 'FSCN|Food Science and Nutrition - FSCN', 'FR|Forest Resources - FR', 'FREN|French - FREN', 'FRIT|French and Italian - FRIT', 'GLBT|Gay, Lesbian, Bisexual, and Transgender Studies - GLBT', 'GWSS|Gender, Women, and Sexuality Studies - GWSS', 'GEND|General Dentistry - GEND', 'GCD|Genetics, Cell Biology and Development - GCD', 'GIS|Geographic Information Science - GIS', 'GEOG|Geography - GEOG', 'GEOE|Geological Engineering - GEOE', 'GEO|Geology and Geophysics - GEO', 'GERI|Geriatrics - GERI', 'GER|German - GER', 'GSD|German,Scandinavian, and Dutch - GSD', 'GERO|Gerontology - GERO', 'GLOS|Global Studies - GLOS', 'GRAD|Graduate School - GRAD', 'GDES|Graphic Design - GDES', 'GRK|Greek - GRK', 'HINF|Health Informatics - HINF', 'HSM|Health Systems Management - HSM', 'HEBR|Hebrew - HEBR', 'HNUR|Hindi and Urdu - HNUR', 'HIST|History - HIST', 'HMED|History of Medicine - HMED', 'HSCI|History of Science and Technology - HSCI', 'HMNG|Hmong - HMNG', 'HCOL|Honors Colloquia - HCOL', 'HSEM|Honors Seminar - HSEM', 'HORT|Horticultural Science - HORT', 'HSG|Housing Studies - HSG', 'HUMF|Human Factors - HUMF', 'HRD|Human Resource Development - HRD', 'HRIR|Human Resources and Industrial Relations - HRIR', 'HUM|Humanities - HUM', 'ICEL|Icelandic - ICEL', 'IE|Industrial Engineering - IE', 'INET|Information Networking - INET', 'IDSC|Information and Decision Sciences - IDSC', 'ISE|Infrastructure Systems Engineering - ISE', 'IS|Innovation Studies - IS', 'INS|Insurance and Risk Management - INS', 'IBH|Integrated Behavioral Health - IBH', 'ICP|Inter-College Program - ICP', 'ID|Interdepartmental Study - ID', 'INAR|Interdisciplinary Archaeological Studies - INAR', 'INMD|Interdisciplinary Medicine - INMD', 'IDES|Interior Design - IDES', 'IBUS|International Business - IBUS', 'IREL|Interpersonal Relationships Research - IREL', 'ISG|Introduced Species and Genotypes - ISG', 'ITAL|Italian - ITAL', 'JPN|Japanese - JPN', 'JWST|Jewish Studies - JWST', 'JOUR|Journalism and Mass Communication - JOUR', 'KIN|Kinesiology - KIN', 'KOR|Korean - KOR', 'LAMP|Laboratory Medicine and Pathology - LAMP', 'LAAS|Land and Atmospheric Science - LAAS', 'LA|Landscape Architecture - LA', 'LGTT|Language, Teaching, and Technology - LGTT', 'LAT|Latin - LAT', 'LAS|Latin American Studies - LAS', 'LAW|Law School - LAW', 'LASK|Learning and Academic Skills - LASK', 'LS|Liberal Studies - LS', 'LING|Linguistics - LING', 'LM|Logistics Management - LM', 'MGMT|Management - MGMT', 'MOT|Management of Technology - MOT', 'MCOM|Managerial Communications - MCOM', 'MM|Manufacturing Operations Management - MM', 'MT|Manufacturing Technology - MT', 'MKTG|Marketing - MKTG', 'MBA|Master of Business Administration - MBA', 'MBT|Master of Business Taxation - MBT', 'MDP|Master of Development Practice - MDP', 'MATS|Materials Science - MATS', 'MATH|Mathematics - MATH', 'MTHE|Mathematics Education - MTHE', 'ME|Mechanical Engineering - ME', 'MILI|Medical Industry Leadership Institute - MILI', 'MEDC|Medicinal Chemistry - MEDC', 'MED|Medicine - MED', 'MEST|Medieval Studies - MEST', 'MICE|Microbial Engineering - MICE', 'MICB|Microbiology - MICB', 'MICA|Microbiology, Immunology, and Cancer Biology - MICA', 'MIL|Military Science - MIL', 'MDGK|Modern Greek - MDGK', 'MCDG|Molecular Cellular Developmental Biol and Genetics - MCDG', 'MORT|Mortuary Science - MORT', 'MIMS|Moving Image Studies - MIMS', 'MDS|Multidisciplinary Studies - MDS', 'MST|Museum Studies - MST', 'MUS|Music - MUS', 'MUSA|Music Applied - MUSA', 'MUED|Music Education - MUED', 'NPSE|Nanoparticle Science and Engineering - NPSE', 'NR|Natural Resources Science and Management - NR', 'NAV|Naval Science - NAV', 'NEUR|Neurology - NEUR', 'NSC|Neuroscience - NSC', 'NSCI|Neuroscience Department - NSCI', 'NSU|Neurosurgery - NSU', 'NOR|Norwegian - NOR', 'NURS|Nursing - NURS', 'NUTR|Nutrition - NUTR', 'OBST|Obstetrics and Gynecology - OBST', 'OT|Occupational Therapy - OT', 'OCS|Off-Campus Study - OCS', 'OUE|Office of Undergraduate Education - OUE', 'OJIB|Ojibwe - OJIB', 'OMS|Operations and Management Sciences - OMS', 'OPH|Ophthalmology - OPH', 'OBIO|Oral Biology - OBIO', 'OSUR|Oral and Maxillofacial Surgery - OSUR', 'OLPD|Organizational Leadership, Policy and Development - OLPD', 'OTHO|Orthodontics - OTHO', 'ORSU|Orthopaedic Surgery - ORSU', 'OTOL|Otolaryngology - OTOL', 'PATH|Pathology - PATH', 'PDEN|Pediatric Dentistry - PDEN', 'PED|Pediatrics - PED', 'PERO|Periodontics - PERO', 'PHM|Pharmaceutics - PHM', 'PHCL|Pharmacology - PHCL', 'PHAR|Pharmacy - PHAR', 'PHIL|Philosophy - PHIL', 'PE|Physical Education - PE', 'PMED|Physical Medicine and Rehabilitation - PMED', 'PT|Physical Therapy - PT', 'PHYS|Physics - PHYS', 'PHSL|Physiology - PHSL', 'PBS|Plant Biological Sciences - PBS', 'PBIO|Plant Biology - PBIO', 'PLPA|Plant Pathology - PLPA', 'PLSH|Polish - PLSH', 'POL|Political Science - POL', 'PORT|Portuguese - PORT', 'PSTL|Postsecondary Teaching and Learning - PSTL', 'PREV|Preventive Science Minor - PREV', 'PDES|Product Design - PDES', 'PIL|Program for Individualized Learning - PIL', 'PROS|Prosthodontics - PROS', 'PSY|Psychology - PSY', 'PA|Public Affairs - PA', 'PUBH|Public Health - PUBH', 'RAD|Radiology - RAD', 'RRM|Recreation Resource Management - RRM', 'REC|Recreation, Park, and Leisure Studies - REC', 'RSC|Rehabilitation Science - RSC', 'RELS|Religious Studies - RELS', 'RC|Respiratory Care - RC', 'RM|Retail Merchandising - RM', 'RUSS|Russian - RUSS', 'RAS|Russian Area Studies - RAS', 'SCAN|Scandinavian - SCAN', 'SCIC|Scientific Computation - SCIC', 'SLS|Second Language Studies - SLS', 'ST|Security Technologies - ST', 'SW|Social Work - SW', 'SAPH|Social and Administrative Pharmacy - SAPH', 'SACP|Social, Administrative, and Clinical Pharmacy - SACP', 'SOC|Sociology - SOC', 'SENG|Software Engineering - SENG', 'SOIL|Soil, Water, and Climate - SOIL', 'SMLI|Somali - SMLI', 'SPAN|Spanish - SPAN', 'SPPT|Spanish and Portuguese - SPPT', 'SLHS|Speech-Language-Hearing Sciences - SLHS', 'SMGT|Sport Management - SMGT', 'STAT|Statistics - STAT', 'SCB|Stem Cell Biology - SCB', 'SCMC|Studies in Cinema and Media Culture - SCMC', 'SST|Studies of Science and Technology - SST', 'SCO|Supply Chain and Operations - SCO', 'SURG|Surgery - SURG', 'SUST|Sustainability Studies - SUST', 'SAGR|Sustainable Agricultural Systems - SAGR', 'SWAH|Swahili - SWAH', 'SWED|Swedish - SWED', 'TMJP|TMJ/Craniofacial Pain - TMJP', 'TH|Theatre Arts - TH', 'TRAD|Therapeutic Radiology - TRAD', 'TXCL|Toxicology - TXCL', 'TRIN|Translation and Interpreting - TRIN', 'UC|University College - UC', 'URBS|Urban Studies - URBS', 'UROL|Urologic Surgery - UROL', 'VBS|Veterinary & Biomedical Sciences - VBS', 'VCS|Veterinary Clinical Sciences - VCS', 'CVM|Veterinary Medicine - CVM', 'VMED|Veterinary Medicine, Graduate - VMED', 'VPM|Veterinary Population Medicine - VPM', 'WMBA|Warsaw Executive MBA - WMBA', 'WRS|Water Resources Science - WRS', 'WHRE|Work and Human Resource Education - WHRE', 'WRIT|Writing Studies - WRIT', 'YOST|Youth Development and Research - YOST']
	codeFound = False
	codeToUse = ""
	# must replace all spaces with + for querying OneStop
	courseCatBar = courseCat + "|"
	for courseCode in courseCodes:
		if courseCode.startswith(courseCatBar):
			codeToUse = courseCode.replace(" ", "+")
			codeFound = True
			break
	if codeFound:
		webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=" + codeToUse + "&searchCatalogNumber=" + courseNum + "&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=false&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&searchLocations=TCEASTBANK%2CEast+Bank&searchLocations=TCWESTBANK%2CWest+Bank&searchLocations=STPAUL%2CSt.+Paul&campus=UMNTC&search=Search"
		return webUrl
	else:
		raise ValueError("Course code not found: " + courseCat)

try:
	searchUrl = getCourseSearchURL(argCourseCat, argCourseNum)
except ValueError:
	sys.exit("Course code not found: " + argCourseCat)

parser = CourseParser()

print "Fetching data for " + argCourseCat + " from OneStop..."
try:
	rawWebData = str(urllib2.urlopen(searchUrl).read())
except urllib.error.URLError:
	sys.exit("Error accessing OneStop class search. OneStop may be offline.")

parser.feed(rawWebData)
parser.finalize()

courseList = parser.getCourseList()
courses    = parser.getCourseCount()
sections   = parser.getSectionCount()

if courses > 0:
	for courseData in courseList:
		courseInfo  = courseData[0]
		sectionData = courseData[1]
		print "Course:", courseInfo
		print "\tSection info:"
		for sectionInfo in sectionData:
			sectionNum = sectionInfo[0]
			seatsAvail = sectionInfo[1]
			seatsTotal = sectionInfo[2]
			if seatsAvail == -1 or seatsTotal == -1:
				print "\t\t" + str(sectionNum) + ": No seats available" 
			else:
				if seatsTotal == 1:
					txtSeatsAvail = "seat available"
				else:
					txtSeatsAvail = "seats available"
				print "\t\t" + str(sectionNum) + ":", seatsAvail, "of", seatsTotal, txtSeatsAvail
				# fallback print function; failures re: seat nos w/o sect. nos should be fixed
				# print("\t\t" + repr(sectionInfo))

if courses == 1:
	txtCourses = "course,"
else:
	txtCourses = "courses,"

if sections == 1:
	txtSections = "section found."
else:
	txtSections = "sections found."

print courses, txtCourses, sections, txtSections