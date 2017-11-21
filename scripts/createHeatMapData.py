#!/usr/local/bin/python3 -u

import sys
import csv
#{location: new google.maps.LatLng(37.782, -122.447), weight: 0.5},
 
 
with open(sys.argv[1], 'r') as f:
	csvfile = csv.reader(f) # pass the file to our csv reader

	for row in csvfile:
		if len(row) == 4:
			value=int(row[1]) * 100
			print('{location: new google.maps.LatLng(' + row[3] + ', ' + row[2] + '), weight: ' + str(value) + '},')
