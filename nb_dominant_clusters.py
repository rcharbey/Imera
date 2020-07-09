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
		
		dominant_clusters = []
		self.dominants_clusters = {}
		prev_cluster, nb_dom_months = -1, 0
		first_month = -1
		order_dominant_cluster = 0
		
		for month in self.months:
			
			cluster, ratio = self.dom_clusters[month]
			
			if prev_cluster != cluster:
				nb_dom_months = 0
			
			if ratio >= self.dom_threshold:
				
				if first_month == -1:
					first_month = month
				
				nb_dom_months += 1
				if nb_dom_months >= 6:	
					if cluster == -1:
						continue
					if not cluster in self.dominants_clusters:
						dominant_clusters.append(cluster)
						self.dominants_clusters[cluster] = {}
					if not first_month in self.dominants_clusters[cluster]:
						order_dominant_cluster += 1
					infos = (order_dominant_cluster, month, nb_dom_months)
					self.dominants_clusters[cluster][first_month] = infos
			else:
				nb_dom_months = 0
				first_month = -1
				
			prev_cluster = cluster
			
		self.nb_dominant_clusters = len(dominant_clusters)
		
	def write_dominant_clusters(self):
		list_clusters = []
		
		if len(self.dominants_clusters) == 0:
			return
	
		for cluster in self.dominants_clusters:
			for first_month in self.dominants_clusters[cluster]:
				order, last_month, duration = self.dominants_clusters[cluster][first_month]
				list_clusters.append((cluster, order, first_month, last_month, duration))
				
		list_clusters.sort(key = lambda x : x[1])
		
		folder = join('..','Results','Dominant_clusters', str(self.dom_threshold) ,'Egos')
		
		if not isdir(folder):
			makedirs(folder)
		
		with open(join(folder, f'{ego}.csv'), 'w') as to_write:
			csvw = csv.writer(to_write)
			csvw.writerow(['dominant_cluster', 'order', 'first_month', 'last_month', 'duration'])
			for cluster in list_clusters:
				csvw.writerow(cluster)
			
				
	def run(self):
		self.read_data()
		self.get_nb_dom_clusters()
		self.write_dominant_clusters()
		return self.nb_dominant_clusters
		

def write_README():
	
	if not isdir(join('..', 'Results', 'Nb_dominant_clusters')):
		makedirs(join('..', 'Results', 'Nb_dominant_clusters'))
		
	if not isdir(join('..', 'Results', 'Dominant_clusters')):
		makedirs(join('..', 'Results', 'Dominant_clusters'))
	
	with open(join('..', 'Results', 'Nb_dominant_clusters', 'README.md'), 'w') as to_write:
		   to_write.write('Chaque CSV contient le nombre de clusters dominants par ego')
		   to_write.write('un cluster est dominant si il publie plus que le second plus actif\n')
		   to_write.write('selon un seuil qui est apparait dans le nom de chaque CSV')
		   to_write.write("champs : 'ego', 'nb_clusters'\n")
		   to_write.write('compute : python3 nb_dominant_clusters [threshold].py \n')
		   
	   
	with open(join('..', 'Results', 'Dominant_clusters', 'README.md'), 'w') as to_write:
		   to_write.write('Chaque sous-dossier correspond à un seuil ')
		   to_write.write('du rapport entre l\'activité du cluster dominant ')
		   to_write.write('et celle du second cluster\n')
		   to_write.write("Chaque CSV contient la liste des clusters dominants successifs \n")
		   to_write.write('un cluster est dominant si il publie plus que le second plus actif\n')
		   to_write.write("champs : id du cluster dominant, ordre d'apparition")
		   to_write.write("premier mois en tant que cluster dominant")
		   to_write.write("dernier mois en tant que cluster dominant")
		   to_write.write("nombre de mois en tant que cluster dominant\n")
		   to_write.write('compute : python3 nb_dominant_clusters.py [threshold] \n')
		   
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
		