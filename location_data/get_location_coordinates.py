import json, requests
from raw_locations import raw_locations

def get_coords():
	geos = []
	url_ = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&components=country&key=AIzaSyC-_i9vKslLONyrw24G6OCKKh4T6VsH65c'
	for each in raw_locations:
		name = each['name'].replace('County', '').replace('Municipio', '')
		state_name = name.split(',')[1]
		try:
			resp = requests.get(url_ % name)
			if resp.status_code == 200:
				result = resp.json()
				lat_long = result['results'][0]['geometry']['location']
				print name, state_name, lat_long
				geos.append({'name': name, 'lat': lat_long['lat'], 'lon': lat_long['lng'], 'state_name': state_name})
		except Exception, e:
			print each
			continue
	f = open('locations_R1.json', 'wb')
	f.write(json.dumps(geos))
	f.close()

#get_coords()
