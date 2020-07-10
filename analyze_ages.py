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
	


if __name__ == '__main__':
	list_thresholds = [1.25, 1.5, 1.75, 2.0, 3.0]
	list_thresholds = [1.25]
	age_per_ego = get_ages()
	age_span_per_ego = get_age_span()
	
	list_all_ages = []
	all_age_min, all_age_max = 1000, 0
	for ego in age_span_per_ego:
		age_min, age_max = age_span_per_ego[ego]
		age_min = int(age_min.split('.')[0])
		age_max = int(age_max.split('.')[0])
		for age in range(age_min, age_max + 1):
			list_all_ages.append(age)
			
			if age < all_age_min:
				all_age_min = age
			if age > all_age_max:
				all_age_max = age
				
	list_all_ages.sort()
	
	result_folder = join('..', 'Results', 'Plot_churns', 'Churns_by_age')
	if not isdir(result_folder):
		makedirs(result_folder)
		
	
	for threshold in list_thresholds:
		
		churner_age_folder = join('..', 'Results', 'Churner_ages')
		list_ages = []
		
		with open(join(churner_age_folder, f'{threshold}.csv'), 'r') as to_read:
			csvr = csv.reader(to_read)
			for line in csvr:
				ego, ages = line[0], [int(x.split('.')[0]) for x in line[1:]]
				for age in ages:
					list_ages.append(age)
		
		list_ages.sort()
		
		
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		bins = [i for i in range(all_age_min, all_age_max + 1)]
		ax1.hist([list_ages, list_all_ages], bins = bins)
		n, bins, patches = ax1.hist([list_ages, list_all_ages], bins = bins)
		plt.cla()
		
		width = (bins[1] - bins[0]) * 0.4
		bins_shifted = bins + width
		#ax2.hist(list_all_ages, color = ['red'], bins = bins_shifted)
		
		print(n[0])
		print(n[1])
		
		ax1.bar(bins[:-1], n[0], width, align='edge', color=['blue'])
		ax2.bar(bins_shifted[:-1], n[1], width, align='edge', color='red')
		
		
		fig_file = f'plot_churns_{threshold}.svg'
		print(threshold)
		plt.tight_layout()
		plt.savefig(join(result_folder, fig_file))
		plt.cla()
		plt.close("all")
			
	
	
