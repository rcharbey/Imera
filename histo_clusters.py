#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:06:32 2020

@author: raphael
"""

import utils
from os.path import isdir, join
from os import makedirs, listdir
import matplotlib.pyplot as plt

data_folder = join('..', 'Data', 'Alter-cluster-timestamp')
age_per_ego = utils.get_ages()
plot_folder = join('..', 'Results', 'Plot_clusters')
if not isdir(plot_folder):
	makedirs(plot_folder)
	
	
slices = [(18,24), (25,39), (40,64), (65,100)]

values_per_slice = {}
for age_slice in slices:
	values_per_slice[age_slice] = []

nb_clusters = []
for ego in listdir(data_folder):
	
	if not ego.split('.')[0][:8] in age_per_ego:
		continue

	data_file = join(data_folder, ego)
	posts_per_cluster = utils.get_posts_per_cluster(data_file)
	nb_clusters.append(len(posts_per_cluster))
	
	age = age_per_ego[ego.split('.')[0][:8]]
	
	for age_slice in slices:
		if age >= age_slice[0] and age <= age_slice[1]:
			values_per_slice[age_slice].append(len(posts_per_cluster))
			print(values_per_slice)
			
	
plt.hist(nb_clusters)
plt.savefig(join(plot_folder, 'nb_active_clusters_per_ego.svg'))
plt.cla()
plt.close("all")

for age_slice in values_per_slice:
	plt.hist(values_per_slice[age_slice])
	plt.savefig(join(plot_folder, f'nb_active_clusters_per_ego_{age_slice}.svg'))
	plt.cla()
	plt.close("all")

