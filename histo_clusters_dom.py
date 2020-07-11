#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:58:42 2020

@author: raphael
"""

import utils
from os.path import isdir, join
from os import makedirs, listdir
import matplotlib.pyplot as plt
import csv
from csv_utils import csv_to_labels

data_folder = join('..', 'Results', 'Nb_dominant_clusters')
age_per_ego = utils.get_ages()
plot_folder = join('..', 'Results', 'Plot_clusters')
if not isdir(plot_folder):
	makedirs(plot_folder)
	
	
slices = [(18,24), (25,39), (40,64), (65,100)]

list_thresholds = [1.25, 1.5, 1.75, 2.0, 3.0]
for threshold in list_thresholds:

	list_nb_dom_clusters = []	
	values_per_slice = {}
	for age_slice in slices:
			values_per_slice[age_slice] = []
	
	
	datafile = join(data_folder, f'nb_clusters_per_ego_{threshold}.csv')
	nb_dom_clusters_per_ego = csv_to_labels(datafile)
	
	for ego in nb_dom_clusters_per_ego:
		if not ego in age_per_ego:
			continue
		age = age_per_ego[ego]
		nb_dom_clusters = int(nb_dom_clusters_per_ego[ego])
		
		
		list_nb_dom_clusters.append(nb_dom_clusters)
		for age_slice in slices:
			if age >= age_slice[0] and age <= age_slice[1]:
				values_per_slice[age_slice].append(nb_dom_clusters)
			
			
	mean_per_age = []		
	for age_slice in slices:
		if len(values_per_slice[age_slice]) == 0:
			mean_per_age.append(0)
			continue
		total = sum(values_per_slice[age_slice])
		mean = total / len(values_per_slice[age_slice])
		mean_per_age.append(mean)
			
	age_slices = ['18-24', '25-29', '40-64', '65+' ]
	
	ax = plt.subplot()
	ax.bar(age_slices, mean_per_age)
		
	plt.savefig(join(plot_folder, f'nb_dom_clusters_per_ego_{threshold}.svg'))
	plt.cla()
	plt.close("all")

