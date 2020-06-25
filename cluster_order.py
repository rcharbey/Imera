#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:34:19 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs, listdir
import csv
import utils


class Cluster_order:
	
	def __init__(self, ego):
		self.data_folder = join('..', 'Data', 'Posts')
		self.result_folder = join('..', 'Results', 'Cluster_order')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		
		self.ego = ego[0:8]
		self.data_file = join(self.data_folder, f'{ego}.csv')
		self.months = set()
		
	
	def read_data(self):
		
		self.posts_per_cluster = utils.get_posts_per_cluster(self.data_file)
		self.months = utils.get_months(self.posts_per_cluster)
		
	def get_cluster_per_month(self):
		
		self.max_cluster_per_month = {}
		
		for month in self.months:
			top_cluster = -1
			top, second = 0, 0
			for cluster in self.posts_per_cluster:
				if cluster == 'ego' or cluster == '-1':
					continue
				cluster_posts = self.posts_per_cluster[cluster].get(month, 0)
				if cluster_posts > top:
					second = top
					top = cluster_posts
					top_cluster = cluster
				elif cluster_posts > second:
					second = cluster_posts
			ratio = top/float(second) if second != 0 else 'inf'
			self.max_cluster_per_month[month] = (top_cluster, ratio)
			
	def write_results(self):
		with open(join(self.result_folder, f'{self.ego}.csv'),'w') as to_write:
			csvw = csv.writer(to_write)
			csvw.writerow(['month', 'first_cluster', 'ratio_over_second'])
			for month in self.months:
				top, ratio = self.max_cluster_per_month[month]
				csvw.writerow([month, top, ratio])
				
	def run(self):
		self.read_data()
		self.posts_per_cluster = utils.smooth_data(self.posts_per_cluster, self.months)
		self.get_cluster_per_month()
		self.write_results()
		

list_egos = [x.split('.')[0] for x in listdir(join('..', 'Data', 'Posts'))]
for ego in list_egos:
	try:
		Cluster_order(ego).run()		
	except:
		print(ego)
			
			