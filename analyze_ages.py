#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 07:40:49 2020

@author: raphael
"""

from utils import get_ages
from os.path import join, isdir
from os import makedirs
from utils import get_ages, get_age_span
import matplotlib.pyplot as plt
import csv
from csv_utils import csv_to_labels


if __name__ == '__main__':
	list_thresholds = [1.25, 1.5, 1.75, 2.0, 3.0]
	age_per_ego = get_ages()
	age_span_per_ego = get_age_span()
	

	for ego in age_span_per_ego:
		if int(age_per_ego[ego]) < 18 : 
			continue
		print(f'{ego} : {age_span_per_ego[ego]}')
	
	for threshold in list_thresholds:
		
		nb_dom_folder = join('..', 'Results', 'Nb_dominant_clusters')
		nb_dom_file = join(nb_dom_folder, f'nb_clusters_per_ego_{threshold}.csv')
		nb_dom_per_ego = csv_to_labels(nb_dom_file)
		list_egos = [ego for ego in nb_dom_per_ego if int(nb_dom_per_ego[ego]) > 1]
	
		youngs = [ego for ego in age_per_ego if age_per_ego[ego] < 25]
		print(f'prop jeunes : {round(len(youngs) / len(age_per_ego), 2)}')
		
		list_all_ages = []
		all_age_min, all_age_max = 1000, 0
		nb_per_age, nb_churn_per_age = {}, {}
		for ego in list_egos:
			
			if not ego in age_per_ego:
				continue
			
			if int(age_per_ego[ego]) < 18:
				continue
			
			age_min, age_max = age_span_per_ego[ego]
			age_min = int(age_min.split('.')[0])
			age_max = int(age_max.split('.')[0])
			for age in range(age_min, age_max + 1):
				list_all_ages.append(age)
				
				if age < all_age_min:
					all_age_min = age
				if age > all_age_max:
					all_age_max = age
					
				if not age in nb_per_age:
					nb_per_age[age] = 0
					nb_churn_per_age[age] = 0
				nb_per_age[age] += 1	
					
		list_all_ages.sort()
		
		result_folder = join('..', 'Results')
		plot_folder = join(result_folder, 'Plot_churns')
		
		churner_age_folder = join(result_folder, 'Churner_ages')
		list_ages = []
		nb_egos = 0
		nb_young_egos = 0
		
		with open(join(churner_age_folder, f'{threshold}.csv'), 'r') as to_read:
			csvr = csv.reader(to_read)
			for line in csvr:
				ego, ages = line[0], [int(x.split('.')[0]) for x in line[1:]]
				
				if int(age_per_ego[ego]) < 18:
					continue
				
				for age in ages:
					list_ages.append(age)
					nb_churn_per_age[age] += 1
				
				# look if ego is young
				if age_per_ego[ego] < 25:
					nb_young_egos += 1
				nb_egos += 1
		
		list_ages.sort()
		
		prop_young = round(nb_young_egos / nb_egos,2)
		
		
		this_plot_folder = join(plot_folder, 'Brute')		
		if not isdir(this_plot_folder):
			makedirs(this_plot_folder)
		
		fig, ax1 = plt.subplots()
		bins = [i for i in range(all_age_min, all_age_max + 1)]
		ax1.hist([list_ages, list_all_ages], bins = bins)
		n, bins, patches = ax1.hist([list_ages, list_all_ages], bins = bins)
		plt.cla()
		
		width = (bins[1] - bins[0]) * 0.4
		bins_shifted = bins + width
		
		ax1.bar(bins[:-1], n[0], width, align='edge', color='blue')
		ax2 = ax1.twinx()
		ax2.bar(bins_shifted[:-1], n[1], width, align='edge', color='red')
		
		
		fig_file = f'plot_churns_{threshold}.svg'
		
		print(f'seuil = {threshold} - prop of young : {prop_young}')
		plt.tight_layout()
		plt.savefig(join(this_plot_folder, fig_file))
		plt.cla()
		plt.close("all")
		
		
		this_plot_folder = join(plot_folder, 'Norm')		
		if not isdir(this_plot_folder):
			makedirs(this_plot_folder)
			
		
			
		print(this_plot_folder)
		print({age : nb_churn_per_age[age] for age list_ages})
		print({age :nb_per_age[age] for list_ages})
		norm_churn_per_age = []
		for age in range(10, 51):
			if not age in nb_per_age :
				norm_churn_per_age.append(0)
				continue
			if nb_per_age[age] < 10:
				norm_churn_per_age.append(0)
				continue
			norm_churn_per_age.append(100*nb_churn_per_age[age] / nb_per_age[age])
		print(norm_churn_per_age)
			
		plt.bar(range(10, 51), norm_churn_per_age)
		plt.savefig(join(this_plot_folder, fig_file))
			
	
	
