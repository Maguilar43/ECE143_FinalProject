#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlrd
import csv
import os

from datetime import date, datetime

# In[23]:

def open_excel(file):
	print(file.title())
	if file.title().startswith('Excel_Data/~$'):
		# print('Wrong')
		return ['Wrong']
	wb = xlrd.open_workbook(filename=file)
	# print(wb.sheet_names())
	sheets = wb.sheets()
	# sheet = wb.sheet_by_index(idx)
	# print(sheet)

	# print(sheet.row_values(0))
	return sheets

# In[88]:
def create_csv(sheet, prefix, prev_path):
	append_csv_flag = False
	for i in range(0, sheet.nrows):
		title = sheet.row_values(i)[0]
		# print(title)
		# print(sheet.row_values(i+2))
		path = ''
		if title is not None and title.startswith('University'):
			path = title
			if path == 'University of California, San Diego Survey of Parking Space Occupancy Levels':
				path = sheet.row_values(i+1)[0].replace(':','_').replace(' ', '_')
				# print(path)
			else:
				path = path.split("University of California, San Diego Survey of Parking Space Occupancy Levels ")[1].replace(':','_').replace(' ', '_')
			# print(path)
			break
	if path != '':
		path = prefix + path + ".csv"
		prev_path = path
		# print(path + "--------------------------------")
	else:
		path = prev_path
		append_csv_flag = True
		# print(path + "--------------------------------")
	with open(path, 'a', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["year", "quarter", "parking_spaces", "8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm",
					"4pm", "5pm", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"]
		if not append_csv_flag:
			csv_write.writerow(csv_head)
		for i in range(sheet.nrows):
			s = sheet.row_values(i)
			start_word = s[2] if isinstance(s[2], str) and s[1] == '' else s[1]
			# print(start_word)
			if start_word.startswith('Summer') and len(start_word) > 15:
				handleCornerCase(csv_write, s)
				continue

			fall_list = list()
			winter_list = list()

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
			ret_list = list()
			ret_list.append(next_row[0])
			for i in s:
				if i != '':
					ret_list.append(i)
			csv_write.writerow(ret_list)
	return prev_path

# In[86]:
def handleCornerCase(csv_write, s):
	# print('------------------')
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
	csv_write.writerow(summer_list)
	csv_write.writerow(fall_list)
	csv_write.writerow(winter_list)
	csv_write.writerow(spring_list)


# In[16]:
if __name__ == '__main__':
	prefix = 'csv_data/'
	excel_location = 'excel_data/'
	files = os.listdir(excel_location)

	# for s in open_excel(excel_location + '3.1 Occupancy Scripps Institution Of Oceanography-Converted.Xlsx'):
	# 	create_csv(s, '', '')


	for file in files:
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



	# print(open_excel('test1.xlsx')[-1].row_values(5)[1])
	# create_csv(open_excel('test1.xlsx')[-1])

