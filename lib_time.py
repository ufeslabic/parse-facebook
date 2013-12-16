#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
#from lib_output import *
from collections import defaultdict

# converts a string in the format dd/mm/yyyy to python datetime
def str_date_to_datetime(str_date):	
	return datetime.datetime.strptime(str_date, '%d/%m/%Y')

# converts a timestamp to a sting in the format dd/mm/yyyy
def timestamp_to_str_date(str_timestamp):
	return datetime.datetime.fromtimestamp(int(str_timestamp)).strftime('%d/%m/%Y')

# converts a timestamp to a python datetime
def timestamp_to_datetime(str_timestamp):
	return datetime.datetime.fromtimestamp(int(str_timestamp))

# a datetime o a date string in the format dd/mm/yyyy
def datetime_to_str_date(datetime):
	return datetime.strftime('%d/%m/%Y')

# a datetime o a date string in the format dd/mm/yyyy HH
def datetime_to_str_date_hour(datetime):
	return datetime.strftime('%d/%m/%Y %H')

# normalize posts by date by adding the missing days in a range of days.
# eg. if a list of dates has 2 posts in day 17/03/2013 then it skips to 5 posts in 19/03/2013
# the 18/03/2013 data point wouldn't exist, this function fills the empty days with zero
def normalize_posts_by_date(dict_int_dates):
	list_str_dates = dict_int_dates.keys()
	list_str_timestamps = []
	for str_date in list_str_dates:
		timestamp = datetime.datetime.strptime(str_date, '%d/%m/%Y')
		list_str_timestamps.append(timestamp)
	max_date = max(list_str_timestamps)
	time_step = min(list_str_timestamps)
	delta = datetime.timedelta(1)	
	while time_step < max_date:
		str_normal_date = time_step.strftime('%d/%m/%Y')
		if str_normal_date in list_str_dates:
			pass
		else:
			dict_int_dates[str_normal_date] = 0
		time_step = time_step + delta	

# receives a list of timestamp and returns a list of all the days between the minimum and the maximum day
# the returned list is in the format dd/mm/yyyy
def fill_days_list(datetimes_list):	
	max_date = max(datetimes_list)
	delta = datetime.timedelta(1) #one day delta
	complete_dates_list = []
	temp_date = min(datetimes_list)
	while temp_date < max_date:
		complete_dates_list.append(temp_date)
		temp_date = temp_date + delta
	return [datetime_to_str_date(x) for x in complete_dates_list]

# creates the comments per day timeline
def comments_per_day(list_datetime_commments):
	list_str_date = fill_days_list(list_datetime_commments)
	dict_int_str_date = defaultdict(int)
	for str_day in list_str_date:
		dict_int_str_date[str_day] += 0
	for datetime in list_datetime_commments:
		str_date = datetime_to_str_date(datetime)
		dict_int_str_date[str_date] += 1
	return dict_int_str_date

#-----------------------------------------
# receives a list of timestamp and returns a list of all the days between the minimum and the maximum day
# the returned list is in the format dd/mm/yyyy
def fill_hours_list(datetimes_list):	
	max_date = max(datetimes_list)
	delta = datetime.timedelta(seconds=3600) #one day delta
	complete_dates_list = []
	temp_date = min(datetimes_list)
	while temp_date < max_date:
		complete_dates_list.append(temp_date)
		temp_date = temp_date + delta
	return [datetime_to_str_date_hour(x) for x in complete_dates_list]

# creates the comments per day timeline
def comments_per_hour(list_datetime_commments):
	list_str_date = fill_hours_list(list_datetime_commments)
	dict_int_str_date = defaultdict(int)
	for str_day_hour in list_str_date:
		dict_int_str_date[str_day_hour] += 0
	for datetime in list_datetime_commments:
		str_date_hour = datetime_to_str_date_hour(datetime)
		dict_int_str_date[str_date_hour] += 1
	return dict_int_str_date
