#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:24:05 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs
import csv
from scipy.stats import chi2_contingency
	
qualifications = ["is_friend","is_coworker","is_family","is_acquaintance"]

	
def build_folders(folder):
	if not isdir(folder):
		makedirs(folder)
		
		
def write_README(folder):
	with open(join(folder, 'README.md'), 'w') as to_write:
		   to_write.write('Liste des alters qualifiés par ego \n')
		   to_write.write('Pour chaque qualifié est précisé la nature sa relation')
		   to_write.write('avec ego, son cluster et depuis combien de temps ego le connaît \n')
		   to_write.write('champs : alter, is_family, is_coworker, is_friend,')
		   to_write.write('is_acquaintance, since, cluster \n')
		   to_write.write('compute : python3 get_qualified.py \n')
	
		      
def get_qualified(ego):
	cluster_folder = join('..', 'Results', 'Qualified', 'Egos')
	cluster_file = join(cluster_folder, f'{ego}.csv')
	
	qualified_alters = {}
	with open(cluster_file, 'r') as to_read:
		csvr = csv.reader(to_read)
		
		header = next(csvr)
		for line in csvr:
			"element","is_friend","is_coworker","is_family","since","cluster","is_acquaintance"

			alter = line[header.index('element')]
			cluster= line[header.index('cluster')]
			
			qualified_alters[alter] = {'cluster' : cluster, 'qualifications' : []}
			for qualification in qualifications:
				if line[header.index(qualification)] == 'True':
					qualified_alters[alter]['qualifications'].append(qualification)
	
	
	return qualified_alters

	
	
		   
if __name__ == '__main__':
	
	Nabil_folder = join('..', 'Data', 'NABIL')
	clusters_per_ego = {}
	with open(join(Nabil_folder, 'filtered_egos_id.txt.csv') , 'r') as to_read:
		csvr = csv.reader(to_read)
		for line in csvr:
			ego,cluster,month,year,alter_count = line
			if not ego in clusters_per_ego:
				clusters_per_ego[ego] = [cluster]
			else:
				clusters_per_ego[ego].append(cluster)
			
	list_egos = [ego for ego in clusters_per_ego.keys() if len(clusters_per_ego[ego]) == 2]		
			
	folder = join('..', 'Results', 'qualified_cluster_churner')
	#build_folders(folder)
	#write_README(folder)
	cluster_order_per_qualif = {qualification : {1 : 0, 2 : 0} for qualification in qualifications}
	
	for ego in list_egos:
		qualified_alters = get_qualified(ego) 
		for alter in qualified_alters:
			cluster = qualified_alters[alter]['cluster']
			if cluster in clusters_per_ego[ego]:
				cluster_order = clusters_per_ego[ego].index(cluster) + 1
				for qualification in qualified_alters[alter]['qualifications']:
					cluster_order_per_qualif[qualification][cluster_order] += 1
					
	data_for_chi2 = []
	for qualification in qualifications:
		qualif_data = []
		for order in cluster_order_per_qualif[qualification]:
			nb_qualified_order = cluster_order_per_qualif[qualification][order]
			print(f'{qualification} : {nb_qualified_order}')
			qualif_data.append(nb_qualified_order)
		data_for_chi2.append(qualif_data)
		print()
		
	print(chi2_contingency(data_for_chi2))[-1]