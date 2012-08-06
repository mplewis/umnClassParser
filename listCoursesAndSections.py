#!/usr/bin/python3

import urllib.request
from html.parser import HTMLParser
import sys

class CourseParser(HTMLParser):
	def __init__(self):
		# must init HTMLParser with strict = false, or else bad tags will break parser
		super().__init__(strict = False)

		# courseList is a list of currCourseData items, one per course
		self.courseList = []

		# if insideCourseTitle is true, then the script is reading a course title
		#     and should keep track of the data
		# insideCourseTitle is true after <h3 class="courseTitle"> and before </h3>
		self.insideCourseTitle = False

		# currCourseData holds data about each course
		# currently only pulls data in between <h3> </h3> tags
		# appends list [course 4-letter category code (HIST, CSCI, etc),
		#     course number, course title] to end of courseList
		self.currCourseData = []

		# sectionList is a list of sectionData items
		self.sectionList = []

		# if insideCourseData is true, then the script is inside course info and should
		#     keep track of section data
		# insideCourseData is 
		self.insideCourseData = False

		# sectionData holds information about individual course sections
		# list is structured as [courseNum, seatsOpen, seatsTotal]
		# if class is full, seatsOpen and seatsTotal will be -1
		self.sectionData = []

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

courseCodes = ['****|****', 'AHS|Academic Health Center Shared - AHS', 'ACCT|Accounting - ACCT', 'ADDS|Addiction Studies - ADDS', 'ADED|Adult Education - ADED', 'ADPY|Adult Psychiatry - ADPY', 'AEM|Aerospace Engineering and Mechanics - AEM', 'AIR|Aerospace Studies - AIR', 'AFRO|African American and African Studies - AFRO', 'AIM|Agricultural Industries and Marketing - AIM', 'AFEE|Agricultural, Food, and Environmental Education - AFEE', 'AGRO|Agronomy and Plant Genetics - AGRO', 'AMIN|American Indian Studies - AMIN', 'ASL|American Sign Language - ASL', 'AMST|American Studies - AMST', 'ANAT|Anatomy - ANAT', 'ANES|Anesthesiology - ANES', 'ANSC|Animal Science - ANSC', 'ANTH|Anthropology - ANTH', 'ADES|Apparel Design - ADES', 'APST|Apparel Studies - APST', 'ABUS|Applied Business - ABUS', 'APEC|Applied Economics - APEC', 'APSC|Applied Plant Sciences - APSC', 'APS|Applied Professional Studies - APS', 'ARAB|Arabic - ARAB', 'ARCH|Architecture - ARCH', 'ARTS|Art - ARTS', 'ARTH|Art History - ARTH', 'ACL|Arts and Cultural Leadership - ACL', 'AAS|Asian American Studies - AAS', 'ALL|Asian Languages and Literatures - ALL', 'AST|Astronomy - AST', 'BIOC|Biochemistry - BIOC', 'BTHX|Bioethics, Center for - BTHX', 'BINF|Bioinformatics - BINF', 'BIOL|Biology - BIOL', 'BSE|Biology, Society, and Environment - BSE', 'BMEN|Biomedical Engineering - BMEN', 'BPHY|Biophysical Sciences - BPHY', 'BBE|Bioproducts and Biosystems Engineering - BBE', 'BA|Business Administration - BA', 'BLAW|Business Law - BLAW', 'BIE|Business and Industry Education - BIE', 'CAHP|Center for Allied Health Programs - CAHP', 'CSPH|Center for Spirituality and Healing - CSPH', 'CHEN|Chemical Engineering - CHEN', 'CHPH|Chemical Physics - CHPH', 'CHEM|Chemistry - CHEM', 'CHIC|Chicano Studies - CHIC', 'CPSY|Child Psychology - CPSY', 'CAPY|Child and Adolescent Psychiatry - CAPY', 'CHN|Chinese - CHN', 'CE|Civil Engineering - CE', 'CLCV|Classical Civilization - CLCV', 'CNES|Classical and Near Eastern Studies - CNES', 'CLS|Clinical Laboratory Science - CLS', 'CLSP|Clinical Laboratory Sciences Program - CLSP', 'CPMS|Clinical Physiology and Movement Science - CPMS', 'CGSC|Cognitive Science - CGSC', 'CFAN|College of Food, Agri & Natural Resource Sciences - CFAN', 'CLA|College of Liberal Arts - CLA', 'CSE|College of Science and Engineering - CSE', 'COMM|Communication Studies - COMM', 'CL|Comparative Literature - CL', 'CSDS|Comparative Studies in Discourse and Society - CSDS', 'CMB|Comparative and Molecular Biosciences - CMB', 'CMPE|Computer Engineering - CMPE', 'CSCI|Computer Science - CSCI', 'CBIO|Conservation Biology - CBIO', 'CMGT|Construction Management - CMGT', 'CDED|Continuing Dental Education - CDED', 'CSDY|Control Science and Dynamical Systems - CSDY', 'CSCL|Cultural Studies and Comparative Literature - CSCL', 'CI|Curriculum and Instruction - CI', 'DAKO|Dakota - DAKO', 'DNCE|Dance - DNCE', 'DH|Dental Hygiene - DH', 'DT|Dental Therapy - DT', 'DENT|Dentistry - DENT', 'DERM|Dermatology - DERM', 'DES|Design - DES', 'DSSC|Development Studies and Social Change - DSSC', 'DDS|Doctor of Dental Surgery - DDS', 'DTCH|Dutch - DTCH', 'EMS|Early Modern Studies - EMS', 'ESCI|Earth Sciences - ESCI', 'EAS|East Asian Studies - EAS', 'EEB|Ecology, Evolution, and Behavior - EEB', 'ECON|Economics - ECON', 'EDUC|Education - EDUC', 'EDHD|Education and Human Development - EDHD', 'EDPA|Educational Policy and Administration - EDPA', 'EPSY|Educational Psychology - EPSY', 'EE|Electrical and Computer Engineering - EE', 'EMMD|Emergency Medicine - EMMD', 'ENDO|Endodontics - ENDO', 'ESL|English as a Second Language - ESL', 'ENGL|English:  Literature - ENGL', 'ENGW|English: Creative Writing - ENGW', 'ENT|Entomology - ENT', 'ENTR|Entrepreneurship - ENTR', 'ESPM|Environmental Sciences, Policy, and Management - ESPM', 'ECP|Experimental and Clinical Pharmacology - ECP', 'FMCH|Family Medicine and Community Health - FMCH', 'FSOS|Family Social Science - FSOS', 'FINA|Finance - FINA', 'FM|Financial Mathematics - FM', 'FIN|Finnish - FIN', 'FW|Fisheries and Wildlife - FW', 'FSCN|Food Science and Nutrition - FSCN', 'FR|Forest Resources - FR', 'FREN|French - FREN', 'FRIT|French and Italian - FRIT', 'GLBT|Gay, Lesbian, Bisexual, and Transgender Studies - GLBT', 'GWSS|Gender, Women, and Sexuality Studies - GWSS', 'GEND|General Dentistry - GEND', 'GCD|Genetics, Cell Biology and Development - GCD', 'GIS|Geographic Information Science - GIS', 'GEOG|Geography - GEOG', 'GEOE|Geological Engineering - GEOE', 'GEO|Geology and Geophysics - GEO', 'GERI|Geriatrics - GERI', 'GER|German - GER', 'GSD|German,Scandinavian, and Dutch - GSD', 'GERO|Gerontology - GERO', 'GLOS|Global Studies - GLOS', 'GRAD|Graduate School - GRAD', 'GDES|Graphic Design - GDES', 'GRK|Greek - GRK', 'HINF|Health Informatics - HINF', 'HSM|Health Systems Management - HSM', 'HEBR|Hebrew - HEBR', 'HNUR|Hindi and Urdu - HNUR', 'HIST|History - HIST', 'HMED|History of Medicine - HMED', 'HSCI|History of Science and Technology - HSCI', 'HMNG|Hmong - HMNG', 'HCOL|Honors Colloquia - HCOL', 'HSEM|Honors Seminar - HSEM', 'HORT|Horticultural Science - HORT', 'HSG|Housing Studies - HSG', 'HUMF|Human Factors - HUMF', 'HRD|Human Resource Development - HRD', 'HRIR|Human Resources and Industrial Relations - HRIR', 'HUM|Humanities - HUM', 'ICEL|Icelandic - ICEL', 'IE|Industrial Engineering - IE', 'INET|Information Networking - INET', 'IDSC|Information and Decision Sciences - IDSC', 'ISE|Infrastructure Systems Engineering - ISE', 'IS|Innovation Studies - IS', 'INS|Insurance and Risk Management - INS', 'IBH|Integrated Behavioral Health - IBH', 'ICP|Inter-College Program - ICP', 'ID|Interdepartmental Study - ID', 'INAR|Interdisciplinary Archaeological Studies - INAR', 'INMD|Interdisciplinary Medicine - INMD', 'IDES|Interior Design - IDES', 'IBUS|International Business - IBUS', 'IREL|Interpersonal Relationships Research - IREL', 'ISG|Introduced Species and Genotypes - ISG', 'ITAL|Italian - ITAL', 'JPN|Japanese - JPN', 'JWST|Jewish Studies - JWST', 'JOUR|Journalism and Mass Communication - JOUR', 'KIN|Kinesiology - KIN', 'KOR|Korean - KOR', 'LAMP|Laboratory Medicine and Pathology - LAMP', 'LAAS|Land and Atmospheric Science - LAAS', 'LA|Landscape Architecture - LA', 'LGTT|Language, Teaching, and Technology - LGTT', 'LAT|Latin - LAT', 'LAS|Latin American Studies - LAS', 'LAW|Law School - LAW', 'LASK|Learning and Academic Skills - LASK', 'LS|Liberal Studies - LS', 'LING|Linguistics - LING', 'LM|Logistics Management - LM', 'MGMT|Management - MGMT', 'MOT|Management of Technology - MOT', 'MCOM|Managerial Communications - MCOM', 'MM|Manufacturing Operations Management - MM', 'MT|Manufacturing Technology - MT', 'MKTG|Marketing - MKTG', 'MBA|Master of Business Administration - MBA', 'MBT|Master of Business Taxation - MBT', 'MDP|Master of Development Practice - MDP', 'MATS|Materials Science - MATS', 'MATH|Mathematics - MATH', 'MTHE|Mathematics Education - MTHE', 'ME|Mechanical Engineering - ME', 'MILI|Medical Industry Leadership Institute - MILI', 'MEDC|Medicinal Chemistry - MEDC', 'MED|Medicine - MED', 'MEST|Medieval Studies - MEST', 'MICE|Microbial Engineering - MICE', 'MICB|Microbiology - MICB', 'MICA|Microbiology, Immunology, and Cancer Biology - MICA', 'MIL|Military Science - MIL', 'MDGK|Modern Greek - MDGK', 'MCDG|Molecular Cellular Developmental Biol and Genetics - MCDG', 'MORT|Mortuary Science - MORT', 'MIMS|Moving Image Studies - MIMS', 'MDS|Multidisciplinary Studies - MDS', 'MST|Museum Studies - MST', 'MUS|Music - MUS', 'MUSA|Music Applied - MUSA', 'MUED|Music Education - MUED', 'NPSE|Nanoparticle Science and Engineering - NPSE', 'NR|Natural Resources Science and Management - NR', 'NAV|Naval Science - NAV', 'NEUR|Neurology - NEUR', 'NSC|Neuroscience - NSC', 'NSCI|Neuroscience Department - NSCI', 'NSU|Neurosurgery - NSU', 'NOR|Norwegian - NOR', 'NURS|Nursing - NURS', 'NUTR|Nutrition - NUTR', 'OBST|Obstetrics and Gynecology - OBST', 'OT|Occupational Therapy - OT', 'OCS|Off-Campus Study - OCS', 'OUE|Office of Undergraduate Education - OUE', 'OJIB|Ojibwe - OJIB', 'OMS|Operations and Management Sciences - OMS', 'OPH|Ophthalmology - OPH', 'OBIO|Oral Biology - OBIO', 'OSUR|Oral and Maxillofacial Surgery - OSUR', 'OLPD|Organizational Leadership, Policy and Development - OLPD', 'OTHO|Orthodontics - OTHO', 'ORSU|Orthopaedic Surgery - ORSU', 'OTOL|Otolaryngology - OTOL', 'PATH|Pathology - PATH', 'PDEN|Pediatric Dentistry - PDEN', 'PED|Pediatrics - PED', 'PERO|Periodontics - PERO', 'PHM|Pharmaceutics - PHM', 'PHCL|Pharmacology - PHCL', 'PHAR|Pharmacy - PHAR', 'PHIL|Philosophy - PHIL', 'PE|Physical Education - PE', 'PMED|Physical Medicine and Rehabilitation - PMED', 'PT|Physical Therapy - PT', 'PHYS|Physics - PHYS', 'PHSL|Physiology - PHSL', 'PBS|Plant Biological Sciences - PBS', 'PBIO|Plant Biology - PBIO', 'PLPA|Plant Pathology - PLPA', 'PLSH|Polish - PLSH', 'POL|Political Science - POL', 'PORT|Portuguese - PORT', 'PSTL|Postsecondary Teaching and Learning - PSTL', 'PREV|Preventive Science Minor - PREV', 'PDES|Product Design - PDES', 'PIL|Program for Individualized Learning - PIL', 'PROS|Prosthodontics - PROS', 'PSY|Psychology - PSY', 'PA|Public Affairs - PA', 'PUBH|Public Health - PUBH', 'RAD|Radiology - RAD', 'RRM|Recreation Resource Management - RRM', 'REC|Recreation, Park, and Leisure Studies - REC', 'RSC|Rehabilitation Science - RSC', 'RELS|Religious Studies - RELS', 'RC|Respiratory Care - RC', 'RM|Retail Merchandising - RM', 'RUSS|Russian - RUSS', 'RAS|Russian Area Studies - RAS', 'SCAN|Scandinavian - SCAN', 'SCIC|Scientific Computation - SCIC', 'SLS|Second Language Studies - SLS', 'ST|Security Technologies - ST', 'SW|Social Work - SW', 'SAPH|Social and Administrative Pharmacy - SAPH', 'SACP|Social, Administrative, and Clinical Pharmacy - SACP', 'SOC|Sociology - SOC', 'SENG|Software Engineering - SENG', 'SOIL|Soil, Water, and Climate - SOIL', 'SMLI|Somali - SMLI', 'SPAN|Spanish - SPAN', 'SPPT|Spanish and Portuguese - SPPT', 'SLHS|Speech-Language-Hearing Sciences - SLHS', 'SMGT|Sport Management - SMGT', 'STAT|Statistics - STAT', 'SCB|Stem Cell Biology - SCB', 'SCMC|Studies in Cinema and Media Culture - SCMC', 'SST|Studies of Science and Technology - SST', 'SCO|Supply Chain and Operations - SCO', 'SURG|Surgery - SURG', 'SUST|Sustainability Studies - SUST', 'SAGR|Sustainable Agricultural Systems - SAGR', 'SWAH|Swahili - SWAH', 'SWED|Swedish - SWED', 'TMJP|TMJ/Craniofacial Pain - TMJP', 'TH|Theatre Arts - TH', 'TRAD|Therapeutic Radiology - TRAD', 'TXCL|Toxicology - TXCL', 'TRIN|Translation and Interpreting - TRIN', 'UC|University College - UC', 'URBS|Urban Studies - URBS', 'UROL|Urologic Surgery - UROL', 'VBS|Veterinary & Biomedical Sciences - VBS', 'VCS|Veterinary Clinical Sciences - VCS', 'CVM|Veterinary Medicine - CVM', 'VMED|Veterinary Medicine, Graduate - VMED', 'VPM|Veterinary Population Medicine - VPM', 'WMBA|Warsaw Executive MBA - WMBA', 'WRS|Water Resources Science - WRS', 'WHRE|Work and Human Resource Education - WHRE', 'WRIT|Writing Studies - WRIT', 'YOST|Youth Development and Research - YOST']

catSearchTerm = "BIOL"

codeFound = False
codeToUse = ""

print("Searching for:", catSearchTerm)

catSearchTerm += "|"

for code in courseCodes:
	if code.startswith(catSearchTerm):
		codeToUse = code
		codeFound = True
		break

if codeFound == False:
	sys.exit("No course code found for search term " + catSearchTerm)

print("Course code found:", codeToUse)

webUrl = "http://onestop2.umn.edu/courseinfo/viewSearchResults.do?campus=UMNTC&swapNow=N&searchTerm=UMNTC%2C1129%2CFall%2C2012&searchSubjects=" + codeToUse + "&searchCatalogNumber=&searchClassroom=true&searchPrimarilyOnline=true&searchOnline=true&searchOpenSections=true&searchLowerStartTime=00%3A00%2C12%3A00&searchUpperEndTime=23%3A59%2C11%3A59&searchMon=true&searchTue=true&searchWed=true&searchThu=true&searchFri=true&searchSat=true&searchSun=true&searchLowerLevelLimit=0%2C0xxx&searchUpperLevelLimit=9999%2C9xxx&searchLowerCreditLimit=0&searchUpperCreditLimit=9999&searchInstructorName=&searchCourseTitle=&searchSessionCodes=ALL%2CALL&campus=UMNTC&search=Search"
parser = CourseParser()

print("Fetching data...")
rawWebData = str(urllib.request.urlopen(webUrl).read())
parser.feed(rawWebData)

#rawFileData = open("./acctData.html", 'r')
#parser.feed(rawFileData)

courseList = parser.getCourseList()

for course in courseList:
	print("Course:", course[0], course[1])
	print("\t", course[2])

print(len(courseList), "courses found.")