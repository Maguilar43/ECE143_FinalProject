import xlrd
import csv
import os

def open_excel(file):
	'''
	Read data from the excel_data fold

	:param file: str, the file name that should be read
	:return: xlrd.sheets, all sheets of this excel file.
	'''


	print(file.title())
	if file.title().startswith('Excel_Data/~$'):
		# To avoid if there are some program using excel Windows and generating a temporary excel file
		return ['Wrong']
	wb = xlrd.open_workbook(filename=file)
	sheets = wb.sheets()

	return sheets

def create_csv(sheet, prefix, prev_path):
	'''

	Extract useful data with cleaning of useless and then get the .csv files

	:param sheet: the excel sheet
	:param prefix: str, the folder we want to store our csv_data
	:param prev_path: str, the subfolder we classify different data and store them
	:return: str, the csv_data file path name
	'''


	# Using a flag to show whether this sheet is in the same table of the previous one
	# but in a different sheet.
	append_csv_flag = False

	# Iterate all sheets and convert them into useful csv format data
	for i in range(0, sheet.nrows):
		title = sheet.row_values(i)[0]
		path = ''
		if title is not None and title.startswith('University'):
			path = title
			if path == 'University of California, San Diego Survey of Parking Space Occupancy Levels':
				path = sheet.row_values(i+1)[0].replace(':','_').replace(' ', '_')
			else:
				path = path.split("University of California, San Diego Survey of Parking Space Occupancy Levels ")[1].replace(':','_').replace(' ', '_')
			break
	if path != '':
		path = prefix + path + ".csv"
		prev_path = path
	else:
		path = prev_path
		append_csv_flag = True

	# Open the csv data file and append the format data into the csv data file
	with open(path, 'a', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["year", "quarter", "parking_spaces", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm",
					"4pm", "5pm", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"]
		if not append_csv_flag:
			csv_write.writerow(csv_head)
		for i in range(sheet.nrows):
			s = sheet.row_values(i)
			start_word = s[2] if isinstance(s[2], str) and s[1] == '' else s[1]

			# This is a corner case because our migration of pdf files have some small mistakes
			if start_word.startswith('Summer') and len(start_word) > 15:
				handleCornerCase(csv_write, s)
				continue

			fall_list = list()
			winter_list = list()

			# Based on different start word of the line, we write the data into differen lines
			if start_word.startswith('Summer'):
				next_row = sheet.row_values(i + 1)
			elif start_word.startswith('Spring'):
				next_row = sheet.row_values(i - 1)
			elif start_word.startswith('Fall'):
				next_row = sheet.row_values(i)
				fall_list.append(next_row[0])
				winter_list.append(next_row[0])

				for idx, i in enumerate(s):
					if i != '':
						pattern = list()
						if isinstance(i, str):
							pattern = i.split('\n')
						else:
							pattern = [i for x in range(4)]
						if len(pattern) == 2:
							if idx == len(s) - 1:
								pattern = [float(i.strip('%')) / 100.0 for i in pattern]
							fall_list.append(pattern[0])
							winter_list.append(pattern[1])
			else:
				continue
			if len(fall_list) > 1:
				csv_write.writerow(fall_list)
				csv_write.writerow(winter_list)
				continue

			# Using the reture list to get all the data as a list
			# and use this list to generate the csv file

			ret_list = list()
			ret_list.append(next_row[0])
			for i in s:
				if i != '':
					ret_list.append(i)
			csv_write.writerow(ret_list)
	return prev_path

# This function is used to handle mistaken format excel files
def handleCornerCase(csv_write, s):
	'''

	Handling excel files with mistaken format

	:param csv_write: the csv file we'd love to write our data into
	:param s: the values we want to add into our csv data files
	:return: None
	'''
	summer_list = list()
	fall_list = list()
	winter_list = list()
	spring_list = list()

	if s[3] == '':
		return
	for i in range(len(s)):
		if i == 0:
			summer_list.append(s[0])
			fall_list.append(s[0])
			winter_list.append(s[0])
			spring_list.append(s[0])

		if i > 1:
			pattern = list()
			if isinstance(s[i], str):
				temp = s[i].replace('\n', ' ')
				pattern = temp.split(' ')
				if len(pattern) == 1 and pattern[0] == '':
					continue

				while len(pattern) != 4 and len(pattern) != 0:
					temp_data = pattern[-1]
					pattern.append(temp_data)
			else:
				pattern = [s[i] for x in range(4)]

			if i == len(s) - 1 and isinstance(s[i], str):
				pattern = [float(i.strip('%')) / 100.0 if not (i == '#DIV/0!' or i == '') else 0.0 for i in pattern]

			if len(pattern) == 4:
				summer_list.append(pattern[0])
				fall_list.append(pattern[1])
				winter_list.append(pattern[2])
				spring_list.append(pattern[3])

	# Write different quarter's list data into the csv files
	csv_write.writerow(summer_list)
	csv_write.writerow(fall_list)
	csv_write.writerow(winter_list)
	csv_write.writerow(spring_list)


# Fix csv data minor mistake because of the excel formatting error
def fix_minor_mistakes():
	'''
	This function fix minor mistakes of the csv files,
	because some of our excel files have some error
	:return: None
	'''
	prefix = 'csv_data/By-Neighborhood/'
	# file_list = ['Sixth_College__All_Parking_Spaces_Combined.csv',
	# 			 'Science_Research_Park__All_Parking_Spaces_Combined.csv',
	# 			 'North_Torrey_Pines_and_Glider_Port__All_Parking_Spaces_Combined.csv']
	file_list = os.listdir(prefix)
	lines_list = []
	quarter_list = ['Summer', 'Fall', 'Winter', 'Spring']
	for file in file_list:
		if not file.endswith('__All_Parking_Spaces_Combined.csv'):
			continue

		fd = open(prefix + file, 'r')
		line = fd.readline()
		lines = []
		lines.append(line)
		count = 0
		while True:
			line = fd.readline()
			if not line:
				break
			if line[8].isalpha():
				lines.append(line)
				continue
			line = line[0:8] + quarter_list[count % 4] + ',' + line[8:]
			count += 1
			lines.append(line)
		lines_list.append(lines)
		fd.close()

	for file, lines in zip(file_list, lines_list):
		fd = open(prefix + file, 'w')
		for line in lines:
			fd.write(line)
		fd.close()

# The main function to iterate all excel files and then get csv data files
if __name__ == '__main__':
	prefix = 'csv_data/'
	excel_location = 'excel_data/'
	files = os.listdir(excel_location)

	for file in files:
		# Ignore the files that is the 2019's data, because they are in different format and
		# should be handled by other functions
		if file == '2019_data' or file.startswith('Spring2019') or file.startswith('Winter2019'):
			continue

		prev = ''
		for sheet in open_excel(excel_location + file):
			if isinstance(sheet,str):
				break;
			folder = ''
			if file.title().startswith('1'):
				folder = prefix + 'University-wide/'
			elif file.title().startswith('2'):
				folder = prefix + 'By-Location/'
			elif file.title().startswith('3'):
				folder = prefix + 'By-Aera/'
			elif file.title().startswith('4'):
				folder = prefix + 'By-Neighborhood/'
			if not os.path.exists(folder):
				os.makedirs(folder)
			prev = create_csv(sheet, folder, prev)
	fix_minor_mistakes()

