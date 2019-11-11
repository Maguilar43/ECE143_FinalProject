#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlrd
import csv

from datetime import date, datetime

# In[23]:


file = 'test1.xlsx'
# def read_excel():

def open_excel(file):
	wb = xlrd.open_workbook(filename=file)
	print(wb.sheet_names())
	sheet1 = wb.sheet_by_index(1)
	print(sheet1)

	print(sheet1.row_values(5))
	return sheet1

# In[88]:

def create_csv():
	sheet1 = open_excel(file)
	path = "test1.csv"
	with open(path, 'w', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["year", "quarter", "parking_spaces", "8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm",
					"4pm", "5pm", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"]
		csv_write.writerow(csv_head)
		for i in range(sheet1.nrows):
			s = sheet1.row_values(i)

			if s[2].startswith('Summer') and len(s[2]) > 15:
				handleCornerCase(csv_write, s)
				continue

			fall_list = list()
			winter_list = list()

			if s[2].startswith('Summer'):
				next_row = sheet1.row_values(i + 1)
			elif s[2].startswith('Spring'):
				next_row = sheet1.row_values(i - 1)
			elif s[2].startswith('Fall'):
				next_row = sheet1.row_values(i)
				fall_list.append(next_row[0])
				winter_list.append(next_row[0])

				for idx, i in enumerate(s):
					if i != '':
						pattern = i.split('\n')
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


# In[86]:
def handleCornerCase(csv_write, s):
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
			temp = s[i].replace('\n', ' ')
			pattern = temp.split(' ')
			if i == len(s) - 1:
				pattern = [float(i.strip('%')) / 100.0 for i in pattern]
			summer_list.append(pattern[0])
			fall_list.append(pattern[1])
			winter_list.append(pattern[2])
			spring_list.append(pattern[3])
	csv_write.writerow(summer_list)
	csv_write.writerow(fall_list)
	csv_write.writerow(winter_list)
	csv_write.writerow(spring_list)


# In[16]:


create_csv()

