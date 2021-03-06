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
		self.data_folder = join('..', 'Data', 'Alter-cluster-timestamp')
		self.result_folder = join('..', 'Results', 'Plots_cluster_activity_no_smooth', 'Egos')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		
		self.ego = ego
		self.data_file = join(self.data_folder, f'{ego}.csv.gz')
		self.months = set()
		self.ego = ego
		
	def read_data(self):
		
		self.posts_per_cluster = utils.get_posts_per_cluster(self.data_file)
		self.months = utils.get_months(self.posts_per_cluster)
		self.total_post_per_clusters = {}
		for cluster in self.posts_per_cluster:
			total_posts = 0
			for month in self.posts_per_cluster[cluster]:
				total_posts += self.posts_per_cluster[cluster][month]
			self.total_post_per_clusters[cluster] = total_posts
		
	def normalize_data(self):
		
		self.posts_per_cluster.pop('ego', None)
		
		self.result_folder = join('..', 'Results', 'Norm_plots_cluster_activity', 'Egos')
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
		self.result_file = join(self.result_folder, f'{self.ego[:8]}.svg')
		
		fig, ax = plt.subplots()
		
		list_clusters = list(self.posts_per_cluster.keys())
		list_clusters.sort(key = lambda x : self.total_post_per_clusters[x], reverse = True)
		print(list_clusters)
		if 'ego' in list_clusters:
 			list_clusters.pop(list_clusters.index('ego'))
 			list_clusters = ['ego'] + list_clusters
		if '-1' in list_clusters:
 			list_clusters.pop(list_clusters.index('-1'))
 			list_clusters = list_clusters + ['-1']
		
		print(list_clusters)
		for cluster in list_clusters:
			
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
				
				
		ax.legend(loc = 'center right', bbox_to_anchor=(1.3, 0.5))	
		fig.suptitle(ego[:8])
		plt.savefig(self.result_file, bbox_inches="tight", format='svg')
		plt.legend(ego)
		plt.cla()
		plt.close("all")
		
	
	def run(self):
		self.read_data()
		#self.posts_per_cluster = utils.smooth_data(self.posts_per_cluster, self.months)
		#self.normalize_data()
		self.plot()
		

		
def write_README():
	
	if not isdir(join('..', 'Results', 'Plots_cluster_activity')):
		makedirs(join('..', 'Results', 'Plots_cluster_activity'))
		
	with open(join('..', 'Results', 'Plots_cluster_activity', 'README.md'), 'w') as to_write:
		   to_write.write('Figure de l\'activité des clusters au fil du temps \n')
		   #to_write.write('chaque valeur est aggrégée sur 7 mois \n')
		   to_write.write('cluster -1 : individus non alter \n')
		   to_write.write('compute : python3 curve_comments_per_clusters.py \n')

if __name__ == '__main__':		
	
	list_egos = [x.split('.')[0] for x in listdir(join('..', 'Data', 'Alter-cluster-timestamp')) 
				 if '.csv.gz' in x]
	
	write_README()
	for ego in list_egos:
		try:
			Draw_ego(ego).run()
		except:
			print(ego)
			continue