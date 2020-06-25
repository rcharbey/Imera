#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:08:59 2020

@author: raphael
"""

from os import listdir, makedirs
from os.path import join, isdir
from csv_utils import csv_to_dict, labels_to_csv

input_folder = join('..', 'Results', 'Cluster_appearance')
output_folder = join('..', 'Results', 'Clusters_after_x_years')
if not isdir(output_folder):
	makedirs(output_folder)

for ego_file in listdir(input_folder):
	nb_appearance_after_x_years = {}
	days_per_cluster, indics = csv_to_dict(join(input_folder, ego_file))
	
	total_nb_clusters = len(days_per_cluster)
	
	nb_clusters = 0
	nb_days, nb_years = 0, 0
	while nb_clusters < total_nb_clusters:
		nb_days += 365
		nb_years += 1
		nb_clusters = len([cluster for cluster in days_per_cluster
					  if days_per_cluster[cluster]['days_before_appearance'] <= nb_days]) 
		nb_appearance_after_x_years[nb_years] = nb_clusters
		
	labels_to_csv(nb_appearance_after_x_years, join(output_folder, ego_file))
	
		
		