#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:59:55 2020

@author: raphael
"""

from os import listdir
import sys
from os.path import expanduser, join
home = expanduser('~')
sys.path.append(join(home, 'Graphs', 'Scripts'))
from graph_utils import Admin
from indicators import Indicators
Graphs_folder = join('..', 'Data', 'Graphs')
Result_folder = join('..', 'Data', 'Clusters')
import csv

list_graphs = listdir(Graphs_folder)
for i, graphfile in enumerate(list_graphs):
	print(f'{i} {graphfile}')
	
	graphname = graphfile.split('.')[0]
	
	graph = Admin.import_graph(join(Graphs_folder, graphfile))
	communities = Indicators(graph).communities()
	with open(join(Result_folder, f'{graphname}.csv'), 'w') as to_write:
		csvw = csv.writer(to_write)
		csvw.writerow(['alter', 'cluster'])
		for i, community in enumerate(communities):
			for alter in community:
				csvw.writerow([graph.vs[alter]['name'], i])