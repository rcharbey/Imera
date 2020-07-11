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

# list_thresholds = [1.25, 1.5, 1.75, 2.0, 3.0]
# for threshold in list_thresholds:

list_nb_dom_clusters = []	
values_per_slice = {}
for age_slice in slices:
		values_per_slice[age_slice] = []


datafile = join(data_folder, f'nb_clusters_per_ego_2.0.csv')
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
		
		
bins = range(1, 10)

	
plt.hist(list_nb_dom_clusters, bins = bins, align = 'mid')
plt.savefig(join(plot_folder, 'nb_dom_clusters_per_ego.svg'))
plt.cla()
plt.close("all")

for age_slice in values_per_slice:
	plt.hist(values_per_slice[age_slice], bins = bins, align = 'mid')
	plt.savefig(join(plot_folder, f'nb_dom_clusters_per_ego_{age_slice}.svg'))
	plt.cla()
	plt.close("all")

