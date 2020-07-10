#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 08:30:11 2020

@author: raphael
"""

from utils import get_ages
from os.path import join, isdir
from os import makedirs
import csv
from datetime import date

class Age_span():
	
	def __init__(self, ego, age):
		
		self.ego = ego
		self.age = age
	
	def run(self):
		first_month, last_month = '', ''
		cluster_order = join('..', 'Results', 'Cluster_order', 'Egos')
		
		with open(join(cluster_order, f'{self.ego}.csv'), 'r') as to_read:
			csvr = csv.reader(to_read)
			next(csvr)
			for line in csvr:
				if first_month == '':
					first_month = line[0]
				last_month = line[0]
		if last_month == '':
			return -1
		last_year, last_month = last_month.split('_')
		first_year, first_month = first_month.split('_')
		
		first_month = date(int(first_year), int(first_month), 1)
		last_month = max(date(int(last_year), int(last_month), 1), date(2013, 11, 1))
		
		nb_years = (last_month - first_month).days/365
		
		return (round(self.age - nb_years), self.age)

def write_README(folder):
	
	if not isdir(folder):
		makedirs(folder)
	
	with open(join(folder, 'README.md'), 'w') as to_write:
		   to_write.write("CSV contenant l'age d'ego au moment de la premiere et de ")
		   to_write.write("la dernière publication sur son compte \n")
		   to_write.write("champs : 'ego', 'age_begin', 'age_end'\n")
		   to_write.write('compute : python3 age_span.py \n')	

if __name__ == '__main__':
	
	age_span_per_ego = {}
	
	age_per_ego = get_ages()
	for ego in age_per_ego:
		try:
			age_span = Age_span(ego, age_per_ego[ego]).run()
			if age_span == -1:
				continue
			age_span_per_ego[ego] = age_span
			
		except:
			continue
	
	result_folder = join('..', 'Results', 'Age_span')	
	write_README(result_folder)
	
	with open(join(result_folder, 'age_span_per_ego.csv'), 'w') as to_write:
		csvw = csv.writer(to_write)
		for ego in age_span_per_ego:
			begin = age_span_per_ego[ego][0]
			end = age_span_per_ego[ego][1]
			csvw.writerow([ego, begin, end])