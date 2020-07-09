#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:57:53 2020

@author: raphael
"""

from os.path import join, isdir, expanduser
from os import makedirs, listdir
import csv
from datetime import date


class Age_per_cluster():
	
	def __init__(self, ego, age, threshold):
		self.ego = ego
		self.age = age
		self.cluster_order = join('..', 'Results', 'Cluster_order', 'Egos')
		self.churn_folder = join('..', 'Results',
						    'Dominant_clusters', str(threshold), 'Egos')
		
	def get_age_date(self):
		last_month = ''
		if not f'{self.ego}.csv' in listdir(self.cluster_order):
			return -1
		with open(join(self.cluster_order, f'{self.ego}.csv'), 'r') as to_read:
			csvr = csv.reader(to_read)
			next(csvr)
			for line in csvr:
				last_month = line[0]
		if last_month == '':
			return -1
		year, month = last_month.split('_')
		self.age_date = max(date(int(year), int(month), 1), date(2013, 11, 1))
		return 1
		
	def get_churns_dates(self):
		
		self.ages_per_churn = []
		
		with open(join(self.churn_folder, f'{self.ego}.csv'), 'r') as to_read:
			csvr = csv.reader(to_read)
			next(csvr)
			former_cluster = ''
			former_date = ''
			for line in csvr:
				cluster, order, first_month, last_month, duration = line
				if former_cluster == '' or former_cluster == cluster:
					former_cluster = cluster			
					year, month = last_month.split('_')
					former_date = date(int(year), int(month), 1)
					continue
				
				if cluster != former_cluster:
					
					year, month = first_month.split('_')
					this_date = date(int(year), int(month), 1)
					
					mean_date = former_date + ((this_date - former_date) / 2)
					
					nb_years = (self.age_date - mean_date).days / 365 
					age = self.age - nb_years
					
					self.ages_per_churn.append(round(age, 1))
					
					year, month = last_month.split('_')
					former_date = date(int(year), int(month), 1)
					former_cluster = cluster
					
	def run(self):
		if self.get_age_date() == -1:
			return []
		self.get_churns_dates()	
		return self.ages_per_churn		


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



if __name__ == '__main__':		
	
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('threshold', type=float)
	
	args = parser.parse_args()
	threshold = args.threshold
	
	age_per_ego = get_ages()
	
	churns_per_ego = {}
	for ego in age_per_ego:
		ages = Age_per_cluster(ego, age_per_ego[ego], args.threshold).run()
		churns_per_ego[ego] = ages
		
	result_folder = join('..', 'Results', 'Churner_ages')
	if not isdir(result_folder):
		makedirs(result_folder)
	
	with open(join(result_folder, f'{threshold}.csv'), 'w') as to_write:
		csvw = csv.writer(to_write)
		for ego in churns_per_ego:
			if not churns_per_ego[ego]:
				continue
			csvw.writerow([ego] + churns_per_ego[ego])
	

	