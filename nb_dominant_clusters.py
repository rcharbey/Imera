#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:22:37 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs, listdir
import csv
from csv_utils import labels_to_csv


class Nb_dominant_clusters:
	
	def __init__(self, ego, dominance_threshold):
		self.data_folder = join('..', 'Results', 'Cluster_order', 'Egos')
		self.data_file = join(self.data_folder, f'{ego}.csv')
		self.dom_threshold = dominance_threshold
	
	def read_data(self):
		self.dom_clusters = {}
		self.months = []
		with open(self.data_file, 'r') as to_read:
			csvr = csv.reader(to_read)
			next(csvr)
			for line in csvr:
				self.months.append(line[0])
				self.dom_clusters[line[0]] = (line[1], float(line[3]))
		
	def get_nb_dom_clusters(self):
		
		dominant_clusters = set()
		prev_cluster, nb_dom_months = -1, 0
		for month in self.months:
			cluster, ratio = self.dom_clusters[month]
			
			# si l'ancien cluster a ete dominant suffisament longtemps
			# on l'ajoute a la liste des clusters dominants
			if prev_cluster != cluster:
				nb_dom_months = 0
			
			if ratio >= self.dom_threshold:
				nb_dom_months += 1
				if nb_dom_months >= 6:
					dominant_clusters.add(cluster)					
			else:
				nb_dom_months = 0
				
			prev_cluster = cluster
			
		self.nb_dominant_clusters = len(dominant_clusters)
				
	def run(self):
		self.read_data()
		self.get_nb_dom_clusters()
		return self.nb_dominant_clusters
		

def write_README():
	
	if not isdir(join('..', 'Results', 'Nb_dominant_clusters')):
		makedirs(join('..', 'Results', 'Nb_dominant_clusters'))
	
	with open(join('..', 'Results', 'Nb_dominant_clusters', 'README.md'), 'w') as to_write:
		   to_write.write('CSV contenant le nombre de clusters dominants par ego')
		   to_write.write('un cluster est dominant si il publie plus que le second plus actif\n')
		   to_write.write('selon un certain ratio, qui apparait dans le nom du csv\n')
		   to_write.write("champs : 'ego', 'nb_clusters'\n")
		   to_write.write('compute : python3 nb_dominant_clusters [threshold].py \n')
		   
if __name__ == '__main__':		
	
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('threshold', type=float)
	
	args = parser.parse_args()
	threshold = args.threshold
	
	
	list_egos = [x.split('.')[0] for x in listdir(join('..', 'Results', 'Cluster_order', 'Egos'))]
	
	
	write_README()	
	nb_per_ego = {}
	for ego in list_egos:	
		try:
			nb_per_ego[ego] = Nb_dominant_clusters(ego, threshold).run()		
		except:
			print(ego)
			
	result_folder = join('..', 'Results', 'Nb_dominant_clusters')
	result_file = join(result_folder, f'nb_clusters_per_ego_{threshold}.csv')
	labels_to_csv(nb_per_ego, result_file)
		