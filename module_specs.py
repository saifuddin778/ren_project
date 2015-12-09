import random

module_globals = { 'gamma': 37}#random.sample(range(25, 31), 1)[0] }

modules  = {
	'pv_1': {
		'name': 'Yinglee YGE-U72',
		'rated_voc': 45.7,
		'rated_power': 315,
		'rated_isc': 9.12,
		'rated_tcell': 25,
	},
	'pv_2': {
		'name': 'Kyocera KD325GX-LFB',
		'rated_voc': 49.7,
		'rated_power': 325,
		'rated_isc': 8.69,
		'rated_tcell': 25,
	},
	'pv_3': {
		'name': 'Sunmodule Plus SW 280 Mono',
		'rated_voc': 39.5,
		'rated_power': 280,
		'rated_isc': 9.71,
		'rated_tcell': 25,
	},
}