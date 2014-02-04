#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, datetime
from lib_cleaning import remove_punctuation, CUSTOMIZED_STOPWORDS
from lib_output import *
from lib_time import *
from collections import defaultdict

def handle_urls(str_url, dict_int_urls):
	if str_url.startswith("h"):		
		dict_int_urls[str_url] += 1

def handle_hashtags(str_hashtag, dict_int_hashtags):
	str_hashtag = remove_punctuation(str_hashtag)
	if str_hashtag is not None:
		str_hashtag = "#" + str_hashtag.lower()
		dict_int_hashtags[str_hashtag] += 1

def handle_words(str_word, dict_int_words):
	str_word = remove_punctuation(str_word)
	if str_word is not None:
		lower_case_word = str_word.lower()
		if lower_case_word not in CUSTOMIZED_STOPWORDS:
			dict_int_words[lower_case_word] += 1

# reads the words in the post and decides what to do with them		
def read_comment_text(comment_text, dict_int_words, dict_int_hashtags, dict_int_urls):
	comment_words = comment_text.split()
	for word in comment_words:
		if len(word) > 1:
			if word.startswith("http"):
				handle_urls(word, dict_int_urls)
			elif word.startswith("#"):
				handle_hashtags(word, dict_int_hashtags)
			else: #if the word isn't  hashtag, mention or URL it is a common word
				handle_words(word, dict_int_words)

def expands_comments_per_post(dict_likes_count):	
	list_top_comments = []
	for post_id, list_of_comments in dict_likes_count.items():
		for tup_comment_like in list_of_comments:
			list_top_comments.append([post_id, tup_comment_like[0], tup_comment_like[1], tup_comment_like[2]])	
	return list_top_comments	

def replace_comments_id_with_comment_text(list_comments_likes, dict_comment_id_text):
	output = []
	for post_id_comment_id_likes_tuple in list_comments_likes:
		post_id = post_id_comment_id_likes_tuple[0]
		comment_id = post_id_comment_id_likes_tuple[1]
		comment_likes = post_id_comment_id_likes_tuple[2]
		is_reply = post_id_comment_id_likes_tuple[3]
		comment_text = dict_comment_id_text[comment_id]
		output.append([post_id, comment_text, comment_likes, is_reply])
	return output

def replace_post_id_with_post_text(list_comments_likes, dict_post_id_text):
	output = []
	for post_id_comment_id_likes_tuple in list_comments_likes:
		post_id = post_id_comment_id_likes_tuple[0]
		post_text = dict_post_id_text[post_id]
		comment_text = post_id_comment_id_likes_tuple[1]
		comment_likes = post_id_comment_id_likes_tuple[2]
		is_reply = post_id_comment_id_likes_tuple[3]
		output.append([post_text, comment_text, comment_likes, is_reply])
	return output
	
def top_comments(dict_likes_count, dict_comment_id_text, dict_post_id_text):
	all_comments = expands_comments_per_post(dict_likes_count)	
	all_comments = replace_comments_id_with_comment_text(all_comments, dict_comment_id_text)	
	all_comments = replace_post_id_with_post_text(all_comments, dict_post_id_text)	
	all_comments_sorted = sorted(all_comments, key=lambda t:int(t[2]), reverse=True)	
	write_top_comments(all_comments_sorted)
	write_top_comment_replies(all_comments_sorted)

'''

USE ME !!!

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
'''

def comments():		
	dict_int_urls = defaultdict(int)
	dict_int_words = defaultdict(int)	
	dict_int_dates = defaultdict(int)
	dict_int_users = defaultdict(int)
	dict_int_datetime = defaultdict(int)
	dict_int_comments_per_post = defaultdict(int)
	dict_int_hashtags = defaultdict(int)
	dict_str_posts = {}
	dict_str_comments = {}
	dict_popular_comments = {}

	with open('comments.tab', 'rt', encoding="utf8") as csvfile:
		file_csv_in = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
		next(file_csv_in)
		for line in file_csv_in:
			# column zero - post ID:
			post_id = line[0]		
			
			# column one - post source:

			# column two - post message:
			post_message = line[2]
			dict_int_comments_per_post[post_message] += 1
			dict_str_posts[post_id] = post_message

			# already parsed in the comments section
			
			# column three - post published:
			# already parsed in the comments section

			# column four - comment id:
			comment_id = line[4]
			
			# column five - comment by:
			user_id = line[1]
			dict_int_users[user_id] += 1

			# column six - is reply:
			is_reply = line[6]

			# column seven - comment message:
			comment_text = line[7]
			read_comment_text(comment_text, dict_int_words, dict_int_hashtags, dict_int_urls)
			dict_str_comments[comment_id] = comment_text
			
			# column eight - comment_published time:
			str_raw_time = line[8]
			temp_datetime = datetime.datetime.strptime(str_raw_time, "%Y-%m-%dT%H:%M:%S+0000")
			dict_int_datetime[temp_datetime] += 1
			str_temp_date = datetime_to_str_date(temp_datetime)
			dict_int_dates[str_temp_date] += 1

			# column nine - comment_like_count:
			like_count = line[9]
			try:
				dict_popular_comments[post_id].append((comment_id, like_count, is_reply))
			except KeyError:
				dict_popular_comments[post_id] = [(comment_id, like_count, is_reply)]
	

	# OUTPUT TIME!
	top_comments(dict_popular_comments, dict_str_comments, dict_str_posts)
	top_something_to_csv(dict_int_dates, 'posts_per_day.csv', ['date', 'number_of_posts'], reverse=False, sort_key=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	top_something_to_csv(dict_int_hashtags, 'top_hashtags.csv', ['hashtags', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(dict_int_words, 'top_words.csv', ['word', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(dict_int_urls, 'top_urls.csv', ['url', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)

	dict_to_txt_for_wordle(dict_int_words, 'top_WORDS_wordle.txt', sort_key=lambda t:t[1])
	dict_to_txt_for_wordle(dict_int_hashtags, 'top_HASHTAGS_wordle.txt', sort_key=lambda t:t[1])	
	
	cleanup_comments()



