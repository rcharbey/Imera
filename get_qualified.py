#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:38:24 2020

@author: raphael
"""

import json
from os.path import join, isdir
from os import listdir, makedirs
import gzip
from csv_utils import dict_to_csv, csv_to_labels

"""
since : depuis quand l'enquêté connaît son ami
(1 : toujours, 2 : +5 ans, 3 : 1 à 5 ans, 4 : moins d'un an)
"""

class Get_qualified:
	
	def __init__(self, ego):
		self.ego = ego
		self.json_folder = join('JSONS', ego)
		self.qualified_file = join(self.json_folder, 'qualify.json.gz')
		self.cluster_folder = join('GALLERY', 'Cluster_per_alter')
		self.cluster_file = join(self.cluster_folder, f'{ego}.csv')
		
		self.infos_per_qualified = {}
		self.list_relationships =  ['family', 'coworker', 'friend', 'acquaintance']
		self.result_folder = join('Results', 'Qualified', 'Egos')
		if not isdir(self.result_folder):
			makedirs(self.result_folder)
		self.result_file = join(self.result_folder, f'{ego}.csv')
		
	def _is_true(self, str_boolean):
		return str_boolean == 'true'
		
	def get_cluster_per_qualified(self):
		self.cluster_per_alter = csv_to_labels(self.cluster_file)
		
	def read_json(self):
		json_file = gzip.open(self.qualified_file, 'rb')
		for line in json_file:
			qualifieds = json.loads(line)['friends']
			for qualified in qualifieds:
				id_qualified = qualified['user_id']
				data = qualified['data']
				self.infos_per_qualified[id_qualified] = {
					  'since' : data['since']
				}
				infos = self.infos_per_qualified[id_qualified]
				for relationship in self.list_relationships:
					is_relationship = self._is_true(data[relationship])	   
					infos[f'is_{relationship}'] = is_relationship
				
				infos['cluster'] = self.cluster_per_alter[id_qualified]
				
	def write_result(self):
		dict_to_csv(self.infos_per_qualified, self.result_file)
		
	def run(self):
		self.get_cluster_per_qualified()
		self.read_json()
		self.write_result()
	
	
	
def build_folders(folder):
	if not isdir(folder):
		makedirs(folder)
		
def write_README():
	with open(join('Results', 'Qualified', 'README.md'), 'w') as to_write:
		   to_write.write('Liste des alters qualifiés par ego \n')
		   to_write.write('Pour chaque qualifié est précisé la nature sa relation')
		   to_write.write('avec ego, son cluster et depuis combien de temps ego le connaît \n')
		   to_write.write('champs : alter, is_family, is_coworker, is_friend,')
		   to_write.write('is_acquaintance, since, cluster \n')
		   to_write.write('compute : python3 get_qualified.py \n')
		   
if __name__ == '__main__':
	
	folder = join('Results', 'Qualified')
	build_folders(folder)
	write_README()
	
	list_egos =  [x.split('.')[0] for x in listdir('JSONS')]
	for ego in list_egos:
		Get_qualified(ego).run()
										    
