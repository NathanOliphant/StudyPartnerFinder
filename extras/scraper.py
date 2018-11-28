#
# 	Scraper is used to scrape the courses from HSU's course listings.
# 	Example usage: python3 scraper.py --year=yyyy --semester=[Spring/Summer/Fall]
# 	python3 scraper.py --year=2018 --semester=Fall

# BS Code from:
# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# SQLite stuff from:  http://www.sqlitetutorial.net/sqlite-python/insert/

# Pass in the semester and year as params.

# Will need to update if new Subject areas added or if subject areas change.
import sqlite3
from sqlite3 import Error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse
import os


#
class Course(object):
	subject_abbrev = ''
	subject_id = 0

	def __init__(self, subject_abbrev, subject_id):
		self.subject_abbrev = subject_abbrev
		self.subject_id = subject_id


#
def makeCourse(subj, course_id):
	crs = Course(subj, course_id)
	return crs


#
def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	try:
		conn = sqlite3.connect(db_file)
		conn.row_factory = sqlite3.Row
		return conn
	except Error as e:
		print(e)

	return None


def select_all_subjects(conn):
	"""
	Query all rows in the subject table
	:param conn: the Connection object
	:return:
	"""
	cur = conn.cursor()
	cur.execute("SELECT id, name, schedule_abbreviation FROM studygroups_subject")

	rows = cur.fetchall()

	return rows


def check_class_exists(subject_id, cn, subj, instructor, semester, year, conn):
	# If we already have this class, do not add it.
	# Check against subject_id, cNNumber, className,
	# instructor, semester, year.
	sql = ''' SELECT COUNT(*) FROM studygroups_course WHERE subject_id=? AND cn_number=?
		 AND class_name=? AND instructor=? AND semester=? AND year=? AND is_active=1 '''

	cur = conn.cursor()
	cur.execute(sql, (subject_id, cn, subj, instructor, semester, year))

	countValue = cur.fetchone()[0]
	ret = False
	if countValue > 0:
		ret = True

	return ret


def scrape_pages(subject, semester):
	# Our source for HSU Spring courses:
	# https://pine.humboldt.edu/anstud/cgi-bin/filt_schd.pl?relevant=sched_ind_Spring.out

	# Fall courses:
	# https://pine.humboldt.edu/anstud/cgi-bin/filt_schd.pl?relevant=sched_ind_Fall.out
	# Should scrape those pages for links from AIE to ZOO
	# Find all hrefs that start with 'filt_schd.pl?relevant=./cschd/schedFall"
	# Find all hrefs that start with 'filt_schd.pl?relevant=./cschd/schedSpring"
	url_base = 'http://pine.humboldt.edu/anstud/cgi-bin/filt_schd.pl?relevant=./cschd/sched'

	#
	url = '{}{}{}.out'.format(url_base, semester, subject['schedule_abbreviation'])

	#
	# subject_id = subject['id']

	# query the website and return the html to the variable 'page'
	page = urlopen(url)

	# parse the html using beautiful soup and store in variable `soup`
	soup = BeautifulSoup(page, 'html.parser')

	tables = soup.findChildren('table')

	# rows = [row in BeautifulSoup(page).find('table').find_all('tr')]
	# iplist = [row.find('td').getText() for row in rows]

	my_table = tables[0]

	rows = my_table.findChildren(['tr'])

	rows = rows[2:]

	return rows


def add_classes(class_rows, semester, year, subject_id, conn):
	print("In add_classes.  Semester is {}, subject_id is {}, and we have {} class rows.".format(semester, subject_id, len(class_rows)))

	for row in class_rows[:-1]:
		cells = row.findChildren('td')

		# Should be wrapped in a Try/Except, and logging any errors!

		checker = cells[0].string
		if checker is not None:
			checker = checker.replace('<BR>', '').strip()
			checker = checker.replace('&nbsp', '').strip()

			if checker != 'Activity' and checker != '2nd Lec' and checker != 'Laboratory' and checker != '':
				subj = " ".join(checker.split())
				cn = cells[2].string
				if cn is None or cn == 'None':
					cn = 00000
				instructor = cells[10].string
				if instructor is None or instructor == 'None':
					instructor = 'N/A'

				# First check to see if class is already in the database.
				if check_class_exists(subject_id, cn, subj, instructor, semester, year, conn) is False:
					sql = ''' INSERT INTO studygroups_Course(subject_id, cn_number, class_name,
						instructor, semester, year, is_active)
						VALUES(?,?,?,?,?,?,?) '''
					cur = conn.cursor()
					cur.execute(sql, (subject_id, cn, subj, instructor, semester, year, 1))


def main():
	# If not installed in the default location, database path will need to be updated.
	# Should be one directory below the current directory.
	#
	database = os.path.join(os.path.dirname (__file__), os.path.pardir, 'db.sqlite3')

	#
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--semester", help = "Semester to retrieve")
	parser.add_argument("-y", "--year", help = "Year to retrieve", type = int)
	#
	args = parser.parse_args()
	#
	semester = args.semester
	year = args.year

	print("Semester: {} {}".format(semester, year))

	# If semester or year not passed, do not run!!!
	if semester is not None and year is not None:
		# Make sure semester is in Spring, Summer, or Fall.
		if semester.lower() == 'spring':
			semester = 'Spring'
		if semester.lower() == 'summer':
			semester = 'Summer'
		if semester.lower() == 'fall':
			semester = 'Fall'
		if semester.lower() in ('spring', 'summer', 'fall'):
			# create a database connection.
			conn = create_connection(database)

			print("Gathering classes for {} {}".format(semester, year))

			with conn:
				subjects = select_all_subjects(conn)
				print("We have {} subjects.".format(len(subjects)))
				for subject in subjects:
					classes = scrape_pages(subject, semester)
					print("We have {} classes in subject {}.".format(len(classes), subject['name']))
					add_classes(classes, semester, year, subject['id'], conn)
		else:
			# Error.
			print("Invalid semester and year passed in.  Please try again.")
	else:
		print("Usage: python3 scraper.py --year=yyyy --semester=[Spring/Summer/Fall]")
		print("You passed semester {} and year {}".format(semester, year))


if __name__ == '__main__':
	main()
