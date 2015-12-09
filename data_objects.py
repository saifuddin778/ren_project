import sys, os, ast
from bson import ObjectId
from mongo_ import establish_connection

from time import time as tm

from module_specs import module_globals, modules

class heatmap_object(object):
	def __init__(self, object_):
		self.type_ = object_['type_']
		self.pv = modules[object_['pv_panel_selected']]
		self.year_window_selected = object_['year_window_selected']
		self.month_selected = int(object_['month_selected'])

	def get_month_data(self):
		t1 = tm()
		keys = map(lambda p: p+self.year_window_selected, ['solarradiation', 'airtemperature'])
		client = establish_connection()
		res = client.test_.ren_project_data.find(
				{'key': { '$in': keys } }, 
				{ 'data': { '$slice': [self.month_selected-1,  1] } }
			)
		data = self.map_([each for each in res], keys).values()
		client.close()
		t2 = tm()
		print t2 - t1
		return data

	def map_(self, data, keys):
		mapped = {}
		for each in data:
			id_ = each['code']
			key = each['key']
			if each['name'].split(', ')[-1] not in ['AK', 'PR', 'HI']:
				if id_ in mapped:
					mapped[id_][key] = each['data'][0]
					for i in each:
						if i != 'data':
							mapped[id_][i] = each[i]
				else:
					mapped[id_] = {}
					mapped[id_][key] = each['data'][0]
					for i in each:
						if i != 'data':
							mapped[id_][i] = each[i]


			# if len(mapped[id_]) == 9:
		for id_ in mapped:
			solar_radiation = mapped[id_][keys[0]]
			air_temperature = mapped[id_][keys[1]]
			tcell = air_temperature + (module_globals['gamma'] * (solar_radiation/1000))
			#tcell = air_temperature + (float(self.pv['rated_tcell'] - 20)/0.8) * solar_radiation/1000
			voc = self.pv['rated_voc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell']))
			pmax = self.pv['rated_power'] * (1 - 0.005 * (tcell - self.pv['rated_tcell']))
			isc = self.pv['rated_isc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell']))
			mapped[id_]['tcell'] = tcell
			mapped[id_]['voc'] = voc
			mapped[id_]['pmax'] = pmax
			mapped[id_]['isc'] = isc
			mapped[id_]['solarradiation'] = solar_radiation
			mapped[id_]['airtemperature'] = air_temperature
		return mapped

class timeseries_object(object):
	def __init__(self, object_):
		self.type_ = object_['type_']
		self.pv = modules[object_['pv_panel_selected']]
		self.year_window_selected = object_['year_window_selected']
		self.codes = ast.literal_eval(object_['locations_selected'])

	def get_timeseries_data(self):
		
		t1 = tm()
		keys = map(lambda p: p+self.year_window_selected, ['solarradiation', 'airtemperature'])
		client = establish_connection()
		res = client.test_.ren_project_data.find(
				{'key': { '$in': keys }, 'code': {'$in': self.codes}}, 
			)
		#data = self.map_([each for each in res], keys).values()
		data = self.map_([each for each in res], keys).values()
		client.close()
		t2 = tm()
		print t2 - t1
		return data

	def map_(self, data, keys):

		mapped = {}
		
		for each in data:
			id_ = each['code']
			key = each['key']
			if id_ in mapped:
				mapped[id_][key] = each['data']
				for i in each:
					if i != 'data':
						mapped[id_][i] = each[i]
			else:
				mapped[id_] = {}
				mapped[id_][key] = each['data']
				for i in each:
					if i != 'data':
						mapped[id_][i] = each[i]
		#--iterate for each location now
		for k, v in mapped.iteritems():
			voc_ = []
			isc_ = []
			pmax_ = []
			tcell_ = []
			solar_radiation = mapped[k][keys[0]]
			air_temperature = mapped[k][keys[1]]
			for sr, at in zip(solar_radiation, air_temperature):
				tcell = round(at + (module_globals['gamma'] * (float(sr)/1000)), 2)
				voc = round(self.pv['rated_voc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell'])), 2)
				pmax = round(self.pv['rated_power'] * (1 - 0.005 * (tcell - self.pv['rated_tcell'])), 2)
				isc = round(self.pv['rated_isc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell'])), 2)
				voc_.append(voc)
				pmax_.append(pmax)
				isc_.append(isc)
				tcell_.append(tcell)
			mapped[k]['solarradiation'] = solar_radiation
			mapped[k]['airtemperature'] = air_temperature
			mapped[k]['voc'] = voc_
			mapped[k]['pmax'] = pmax_
			mapped[k]['isc'] = isc_
			mapped[k]['tcell'] = tcell_
		return mapped
			



