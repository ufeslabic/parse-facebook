#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys, subprocess
from lib_time import *

# returns the given float number with only 2 decimals and a % appended
def float_to_percentage(float_number):
	return("%0.2f" % float_number +"%")

# normalize the dictionary with the word count to generate the wordcloud
def normalize_dict(dic):
	max_elem = max(dic.values())
	for key, value in dic.items():
		normalized_val = int((100 * value)/max_elem)
		if normalized_val == 0:
			normalized_val = 1
		dic[key]= normalized_val
	return dic


# writes the normalized dict in a txt to be pasted manually in wordle.net
def dict_to_txt_for_wordle(dict_in, filename, sort_key=lambda t:t, value_key=lambda t:t):
	if not dict_in:
		dict_in = {'No hashtags found':1}
	ordered_list = []
	dict_in = normalize_dict(dict_in)
	for key, value in dict_in.items():
		ordered_list.append([key, value_key(value)])
	ordered_list = 	sorted(ordered_list, key=sort_key, reverse=True)
	out = open(filename, 'w', encoding= 'utf-8')
	for item in ordered_list[:120]:
		i = 0
		while i < item[1]:
			out.write(item[0] + ' ')
			i+=1
	out.close()

# creates a CSV file of the dictionary data received
def top_something_to_csv(dict_in, filename, column_titles, reverse, sort_key, value_format=lambda t: t):
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value_format(value)])
	ordered_list = sorted(ordered_list, key=sort_key, reverse=reverse)
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list:
			file_writer.writerow([item[0], item[1]])
		csvfile.close()

# writes a CSV file in the following format:
# post_type | interactions_# | %_of_total
# where interactions can be shares, likes or comments
def int_dictionary_to_csv(int_dict_in, filename, column_titles):
	total = sum(int_dict_in.values())
	float_dict_post_percent = {}
	for key, value in int_dict_in.items():
		float_dict_post_percent[key] = (value * 100)/total
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(column_titles)
		for key, value in float_dict_post_percent.items():
			file_writer.writerow([key, int_dict_in[key], float_to_percentage(value)])

# writes a CSV file in the following format:
# date(dd/mm/yyyy) | post_type | post_text| interactions_#
# where interactions can be shares, likes or comments and post_type can be status, photo, video or share
def int_dictionary_interactions_summary_to_csv(int_dict_comments_in, int_dict_shares_in, int_dict_likes_in, filename):
	column_titles = ['post_type', 'comments_#', 'comments_%', '', 'likes_#', 'likes_%','', 'shares_#', 'shares_%',]
	total_comments = sum(int_dict_comments_in.values())	
	total_shares = sum(int_dict_shares_in.values())
	total_likes = sum(int_dict_likes_in.values())
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(column_titles)
		for key in int_dict_comments_in.keys():
			pct_comments = (int_dict_comments_in[key]*100)/total_comments
			pct_likes = (int_dict_likes_in[key]*100)/total_likes
			pct_shares = (int_dict_shares_in[key]*100)/total_shares			
			file_writer.writerow([key, int_dict_comments_in[key], float_to_percentage(pct_comments),' ', int_dict_likes_in[key], float_to_percentage(pct_likes), ' ', int_dict_shares_in[key], float_to_percentage(pct_shares)])

# writes a CSV file in the following format:
# dd/mm/YYYY | post_type | post_text | interactions_#
# where interactions can be shares, likes or comments
def interactions_summary_to_csv(list_summary, filename, column_titles):
	list_summary = sorted(list_summary, key = lambda x: x[0])
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(column_titles)
		for item in list_summary:
			line = [timestamp_to_str_date(item[0])] + item[1:]
			file_writer.writerow(line)

# creates a CSV file of the dictionary data received
def top_something_to_csv(dict_in, filename, column_titles, reverse, sort_key, value_format=lambda t: t):
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value_format(value)])
	ordered_list = sorted(ordered_list, key=sort_key, reverse=reverse)
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list:
			file_writer.writerow([item[0], item[1]])
		csvfile.close()

def comments_timeline():
	list_datetime_commments = []
	with open('comments.tab', 'rt', encoding="utf8") as csvfile:
		csv_in = csv.reader(csvfile, delimiter='\t')
		next(csv_in)
		for line in csv_in:
			str_raw_time = line[3]
			temp_datetime = datetime.datetime.strptime(str_raw_time, "%Y-%m-%dT%H:%M:%S+0000")
			list_datetime_commments.append(temp_datetime)
			dict_int_str_date = comments_per_day(list_datetime_commments)
			dict_int_str_date_hour = comments_per_hour(list_datetime_commments)
	top_something_to_csv(dict_int_str_date, 'comments_per_day.csv', ['date', 'number_of_comments'], reverse=False, sort_key=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	top_something_to_csv(dict_int_str_date_hour, 'comments_per_hour.csv', ['date', 'number_of_comments'], reverse=False, sort_key=lambda t: datetime.datetime.strptime(t[0], "%d/%m/%Y %H"))


def write_top_comment_replies(top_comments_list):
	with open('top_comments_replies.csv', 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['post_text', 'comment_text', 'likes_#'])
		for item in top_comments_list:
			if item[3] == '1':
				file_writer.writerow([item[0], item[1], item[2]])

def write_top_comments(top_comments_list):
	with open('top_comments.csv', 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['post_text', 'comment_text', 'likes_#', 'is_reply'])
		for item in top_comments_list:
			file_writer.writerow(item)

def cleanup_posts():
	subprocess.call(["sh", "cleanup_posts.sh"])

def cleanup_comments():
	subprocess.call(["sh", "cleanup_comments.sh"])