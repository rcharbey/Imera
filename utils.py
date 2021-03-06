#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:48:36 2020

@author: raphael
"""

import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import gzip
from os.path import join

		
def date_to_str(date):
	month = date.month
	year = date.year
	if month >= 10:
		date_str = f'{year}_{month}'
	else:
		date_str = f'{year}_0{month}'
	return date_str


def get_posts_per_cluster(data_file):
	
	posts_per_cluster = {}
	
	with gzip.open(data_file, 'rt') as to_read:
		csvr = csv.reader(to_read)
		next(csvr)
		for line in csvr:
			author,cluster,timestamp,status,comment = line
			
			if not cluster in posts_per_cluster:
				posts_per_cluster[cluster] = {}
			
			date = datetime.fromtimestamp(int(timestamp))
			date_str = date_to_str(date)
			
			if not date_str in posts_per_cluster[cluster]:
				posts_per_cluster[cluster][date_str] = 0
				
			posts_per_cluster[cluster][date_str] += 1
		
	return posts_per_cluster

def get_months(post_list):
	
	months = set()
	for cluster in post_list:
		months.update(list(post_list[cluster].keys()))
	months = list(months)
	months.sort()
	
	return months

				
				
def smooth_data(data, months):
	
	smooth_data = {}
	
	for cluster in data:
		smooth_data[cluster] = {}
		
		for date_str in months:
			old_value = data[cluster].get(date_str, 0)
			smooth_data[cluster][date_str] = old_value
			
		for date_str in months:
			year, month = date_str.split('_')
			date = datetime(day = 1, year = int(year), month = int(month))
			
			sum_neighbors = 0
			for i in range(-4, 4):
				if i == 0 : 
					continue
				use_date = date + relativedelta(months=i)
				nei_date_str = date_to_str(use_date)
				sum_neighbors += data[cluster].get(nei_date_str, 0)
				
			smooth_data[cluster][date_str] += sum_neighbors
			
	return smooth_data


def get_ages():
	age_per_ego = {}
	with open(join('AGE_FOLDER','egos-age-gender-profession.csv'), 'r') as to_read:
		csvr = csv.reader(to_read)
		for line in csvr:
			try:
				age_per_ego[line[0]] = int(line[1])
			except:
				continue
	return age_per_ego

def get_age_span():
	age_span_per_ego = {}
	with open(join('..', 'Results', 'Age_span', 'age_span_per_ego.csv'), 'r') as to_read:
		csvr = csv.reader(to_read)
		for line in csvr:
			try:
				age_span_per_ego[line[0]] = (line[1], line[2])
			except:
				continue
	return age_span_per_ego