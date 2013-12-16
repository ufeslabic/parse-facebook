#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, datetime
from lib_time import *
from lib_output import *
from lib_comments import *
from lib_cleaning import *
from collections import defaultdict

def count_post_type(post_type, dict_int_total_post_types):
	dict_int_total_post_types[post_type] += 1

def count_posts_by_date(str_normal_date, dict_int_dates):
	dict_int_dates[str_normal_date] += 1

def interactions_summary(timestamp, post_type, post_message, number_of_interactions, interactions_list):
	interactions_list.append([timestamp, post_type, post_message, number_of_interactions])

def interactions_summary_global(timestamp, post_type, post_message, num_comments, num_likes, num_shares, interactions_list):
	interactions_list.append([timestamp, post_type, post_message, num_comments, num_likes, num_shares])

def handle_urls(str_url, dict_int_urls):
	if str_url.startswith("h"):		
		dict_int_urls[str_url] += 1

def handle_hashtags(str_hashtag, dict_int_hashtags):
	str_hashtag = "#" + remove_punctuation(str_hashtag) 
	dict_int_hashtags[str_hashtag] += 1

def handle_words(str_word, dict_int_words):
	lower_case_word = str_word.lower()
	clean_word = remove_punctuation(lower_case_word)
	if clean_word not in stopwords:
		dict_int_words[clean_word] += 1

# reads the words in the post and decides what to do with them		
def read_post_text(post_text, dict_int_words, dict_int_hashtags):
	post_words = post_text.split()
	for word in post_words:
		if len(word) > 1:
			if word.startswith("#"):
				handle_hashtags(word, dict_int_hashtags)
			else: #if the word isn't  hashtag, mention or URL it is a common word
				handle_words(word, dict_int_words)

def posts():		
	dict_int_urls = defaultdict(int)
	dict_int_words = defaultdict(int)	
	dict_int_dates = defaultdict(int)
	dict_int_hashtags = defaultdict(int)
	dict_int_total_post_types = defaultdict(int)
	dict_int_likes_by_post_types = defaultdict(int)
	dict_int_shares_by_post_types = defaultdict(int)
	dict_int_comments_by_post_types = defaultdict(int)	
	dict_dict_post_source_type = {'users': defaultdict(int), 'page': defaultdict(int)}	

	likes_summary = []
	shares_summary = []
	global_summary = []
	comments_summary = []	
	
	with open('stats.tab', 'rt', encoding="utf8") as csvfile:
		csv_in = csv.reader(csvfile, delimiter='\t')
		next(csv_in)
		for line in csv_in:
			# column zero - post type:
			post_type = line[0]
			count_post_type(post_type, dict_int_total_post_types)			
			
			# column one - post source:

			# column two - post message:
			post_message = line[2]
			read_post_text(post_message, dict_int_words, dict_int_hashtags)

			# column three - post thumbnail:

			# column four - linked content:
			str_link_complete = line[4]
			handle_urls(str_link_complete, dict_int_urls)

			# column five - link domain:			

			# column six - date published:
			# ignored, timestamp is used instead

			# column seven - timestamp of the published date:
			timestamp = line[7]
			normal_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
			count_posts_by_date(normal_date, dict_int_dates)
			
			#count_posts_types_by_date(normal_date, post_type, dict_dict_dates)

			# column eight - likes:
			likes = line[8]
			dict_int_likes_by_post_types[post_type] += int(line[8])
			# column nine - likes_count_fb:

			# column ten - comments_all:
			comments_all = line[10]
			dict_int_comments_by_post_types[post_type] += int(line[10])

			# column eleven - comments_base:

			# column twelve - comments_replies:

			# column thirteen - shares:
			shares = line[13]
			try:
				dict_int_shares_by_post_types[post_type] += int(line[13])
			except ValueError:
				dict_int_shares_by_post_types[post_type] += 0

			# column fourteen - comment_likes:			

			# column fifteen - engagement:

			# column sixteen - post_id:	

			# column seventeen - post_link:			
			
			interactions_summary(timestamp, post_type, post_message, comments_all, comments_summary)
			interactions_summary(timestamp, post_type, post_message, likes, likes_summary)
			interactions_summary(timestamp, post_type, post_message, shares, shares_summary)
			interactions_summary_global(timestamp, post_type, post_message, comments_all, likes, shares, global_summary)
	
	normalize_posts_by_date(dict_int_dates)

	# OUTPUT TIME!	
	interactions_summary_to_csv(comments_summary, 'post_COMMENTS.csv', ['date', 'post_type', 'post_text', 'comments_#'])
	interactions_summary_to_csv(likes_summary, 'post_LIKES.csv', ['date', 'post_type', 'post_text', 'likes_#'])
	interactions_summary_to_csv(shares_summary, 'post_SHARES.csv', ['date', 'post_type', 'post_text', 'shares_#'])
	interactions_summary_to_csv(global_summary, 'post_GLOBAL.csv', ['date', 'post_type', 'post_text', 'comments_#', 'likes_#', 'shares_#'])	
	
	int_dictionary_to_csv(dict_int_total_post_types, 'post_type_distribution.csv', ['post_type', 'post_count', 'post_%'])
	int_dictionary_to_csv(dict_int_likes_by_post_types, 'post_LIKES_by_type.csv', ['post_type', 'likes', 'post_%'])
	int_dictionary_to_csv(dict_int_shares_by_post_types, 'post_SHARES_by_type.csv', ['post_type', 'shares', 'post_%'])
	int_dictionary_to_csv(dict_int_comments_by_post_types, 'post_COMMENTS_by_type.csv', ['post_type', 'comments', 'post_%'])
	int_dictionary_interactions_summary_to_csv(dict_int_comments_by_post_types, dict_int_shares_by_post_types, dict_int_likes_by_post_types, 'interactions_summary.csv')	
	
	top_something_to_csv(dict_int_dates, 'posts_per_day.csv', ['date', 'number_of_posts'], reverse=False, sort_key=lambda t: datetime.date(int(t[0][6:]), int(t[0][3:5]), int(t[0][:2])))
	top_something_to_csv(dict_int_hashtags, 'top_hashtags.csv', ['hashtags', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(dict_int_words, 'top_words.csv', ['word', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)
	top_something_to_csv(dict_int_urls, 'top_urls.csv', ['url', 'times_mentioned'], True, sort_key=lambda t: t[1], value_format=lambda t:t)

	dict_to_txt_for_wordle(dict_int_words, 'top_WORDS_wordle.txt', sort_key=lambda t:t[1])
	dict_to_txt_for_wordle(dict_int_hashtags, 'top_HASHTAGS_wordle.txt', sort_key=lambda t:t[1])
	cleanup_posts()


