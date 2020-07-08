#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:24:05 2020

@author: raphael
"""

from os.path import join, isdir
from os import makedirs
from csv_utils import csv_to_dict


	
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
	return csv_to_dict(cluster_file)

	
	
		   
if __name__ == '__main__':
	
	import csv
	
	Nabil_folder = join('..', 'Data', 'NABIL')
	clusters_per_ego = {}
	with open(join(Nabil_folder, 'filtered_egos_month_year_cluster_altercount.csv') , 'r') as to_read:
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
	
	qualifications = ["is_friend","is_coworker","is_family","is_acquaintance"]
	cluster_order_per_qualif = {qualification : {1 : 0, 2 : 0} for qualification in qualifications}
	
	for ego in list_egos:
		qualified_alters, header = get_qualified(ego)
		for alter in qualified_alters:
			cluster = alter[cluster]
			if cluster in clusters_per_ego[ego]:
				cluster_order = clusters_per_ego[ego].index(cluster) + 1
				print(alter)
				for qualification in qualifications:
					if qualified_alters[qualification]:
						cluster_order_per_qualif[qualification][cluster_order] += 1
		