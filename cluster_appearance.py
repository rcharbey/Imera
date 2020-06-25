#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:53:33 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs, listdir
import csv
from datetime import datetime

class Cluster_appearance:
	
	def __init__(self, ego):
		self.data_folder = join('..', 'Data', 'Posts')
		self.result_folder = join('..', 'Results', 'Cluster_appearance')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		
		self.ego = ego[0:8]
		self.data_file = join(self.data_folder, f'{ego}.csv')
		self.first_message = None
		
	
	def read_data(self):
		
		self.first_by_cluster = {}
		
		with open(self.data_file, 'r') as to_read:
			csvr = csv.reader(to_read)
			next(csvr)
			for line in csvr:
				author,cluster,timestamp,status,comment = line
				
				timestamp = datetime.fromtimestamp(int(timestamp))
				
				if self.first_message == None:
					self.first_message = timestamp
				self.first_message = min(timestamp, self.first_message)
				
				if cluster == 'ego' or cluster == '-1':
					continue
				
				if not cluster in self.first_by_cluster:
					self.first_by_cluster[cluster] = timestamp
				if timestamp < self.first_by_cluster[cluster]:
					self.first_by_cluster[cluster] = timestamp
					
					
			
	def write_results(self):
		
		with open(join(self.result_folder, f'{self.ego}.csv'), 'w') as to_write:
			csvw = csv.writer(to_write, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
			csvw.writerow(['cluster', 'days_before_appearance'])
			for cluster in self.first_by_cluster:
				nb_days = (self.first_by_cluster[cluster] - self.first_message).days
				csvw.writerow([cluster, nb_days])
				
	def run(self):
		self.read_data()
		self.write_results()
				
		
list_egos = [x.split('.')[0] for x in listdir(join('..', 'Data', 'Posts'))]
for ego in list_egos:
	try:
		Cluster_appearance(ego).run()		
	except:
		print(ego)