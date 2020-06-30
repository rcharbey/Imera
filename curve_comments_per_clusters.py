#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:10:27 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs, listdir
import matplotlib.pyplot as plt
import utils

class Draw_ego:
	
	def __init__(self, ego):
		self.data_folder = join('..', 'Data', 'Posts')
		self.result_folder = join('..', 'Results', 'Posts', 'Plot')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		
		self.ego = ego
		self.data_file = join(self.data_folder, f'{ego}.csv')
		self.months = set()
		self.ego = ego
		
	def read_data(self):
		
		self.posts_per_cluster = utils.get_posts_per_cluster(self.data_file)
		self.months = utils.get_months(self.posts_per_cluster)
		
	def normalize_data(self):
		
		self.posts_per_cluster.pop('ego', None)
		
		self.result_folder = join('..', 'Results', 'Posts', 'Norm_Plot')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		
		for month in self.months:
			sum_month = sum([self.posts_per_cluster[cluster].get(month, 0) 
					for cluster in self.posts_per_cluster])
			
			for cluster in self.posts_per_cluster:
				if not month in self.posts_per_cluster[cluster]:
					continue
				self.posts_per_cluster[cluster][month] /= sum_month
				
					
 				
	def plot(self):
		self.result_file = join(self.result_folder, f'{self.ego}.svg')
		
		fig, ax = plt.subplots()
		
		for cluster in self.posts_per_cluster:
			
			x, y = [], []
			
			for date_str in self.months:
				x.append(date_str)
				y.append(self.posts_per_cluster[cluster].get(date_str, 0))
			
			linestyle = 'dotted' if cluster == 'ego' else 'solid'
			plt.plot(x, y, linestyle = linestyle, label=cluster)	
			
		plt.xticks(fontsize=6, rotation=60)
				
		every_nth = 6
		for n, label in enumerate(ax.xaxis.get_ticklabels()):
		    if n % every_nth != 0:
		        label.set_visible(False)
				
				
		lgd = ax.legend(loc = 'center right', bbox_to_anchor=(1.3, 0.5))				
			
		print(self.result_file)
		plt.savefig(self.result_file, bbox_inches="tight")
		
	
	def run(self):
		self.read_data()
		self.posts_per_cluster = utils.smooth_data(self.posts_per_cluster, self.months)
		#self.normalize_data()
		self.plot()
		
list_egos = [x.split('.')[0] for x in listdir(join('..', 'Data', 'Posts'))]

for ego in list_egos:
	try:
		Draw_ego(ego).run()
	except:
		print(ego)
		continue