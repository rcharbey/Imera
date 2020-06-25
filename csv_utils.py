#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:58:56 2020

@author: raphael
"""

import csv

def csv_to_dict(csvfile):
	result = {}
	with open(csvfile, 'r') as to_read:
		csvr = csv.reader(to_read, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
		indics = next(csvr)[1:]
		for line in csvr:
			element, values = line[0], line[1:]
			result[element] = {}
			for i, value in enumerate(values):
				result[element][indics[i]] = float(value)
	return result, indics

def csv_to_labels(csvfile):
	labels = {}
	with open(csvfile, 'r') as to_read:
		csvr = csv.reader(to_read, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
		next(csvr)
		for line in csvr:
			labels[line[0]] = line[1]
	return labels	


def get_second_dictionnary_fields(dictionnary):
	result = set()
	for element in dictionnary:
		for key in dictionnary[element].keys():
			result.add(key)
	return list(result)

def labels_to_csv(labels, csvfile):
	with open(csvfile, 'w') as to_write:
		csvw = csv.writer(to_write, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
		csvw.writerow(['element', 'label'])
		for element in labels:
			csvw.writerow([element, labels[element]])
	

def dict_to_csv(dictionnary, csvfile):
	with open(csvfile, 'w') as to_write:
		csvw = csv.writer(to_write, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
		fields = get_second_dictionnary_fields(dictionnary)
		csvw.writerow(['element'] + fields)
		for element in dictionnary.keys():
			row = [element]
			for field in fields:
				row.append(dictionnary[element].get(field, ''))
			csvw.writerow(row)
			
def dok_to_csv(dok, features, csvfile):
	with open(csvfile, 'w') as to_write:
		csvw = csv.writer(to_write)
		csvw.writerow([''] + features)
		for i, feature in enumerate(features):
			row = [feature]
			for j in range(len(features)):
				row.append(dok[i, j])
			csvw.writerow(row)
				

def transpose_csv(csvfile):
	result = {}
	dictionnary = csv_to_dict(csvfile)
	fields = get_second_dictionnary_fields(dictionnary) 
	for field in fields:
		result[field] = {}
		for element in dictionnary:
			result[field][element] = dictionnary[element].get(field, '')
	return result
			