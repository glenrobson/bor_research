#!/usr/local/bin/python3 -u

import sys
import csv
import googlemaps
import json
import string
import os

def filename(place):
	return place.replace(" ","_").translate(str.maketrans('', '', string.punctuation))

if len(sys.argv) < 3:
    print ("Usage:\n\t%s [locations in csv] [output_csv]" % sys.argv[0])
    os,exit(-1)

print ("Connecting to google")
if os.path.isfile('.googlekey'):
    with open('.googlekey') as fp:  
        key=fp.read().rstrip()
else:
    print ('You must supply a google map key in a file called `.googlekey`')
    os.exit(-1)
print ('key "%s"' % key)           
gmaps = googlemaps.Client(key=key)
print ("Opening csv file")
with open(sys.argv[2], 'w') as csvfile:
	csvout = csv.writer(csvfile,  delimiter=',')
	with open(sys.argv[1], 'r') as f:
		csvfile = csv.reader(f) # pass the file to our csv reader

		for row in csvfile:
			if len(row) > 0:
				newrow = row

				cachefile='cache-place/' + filename(row[0]) + ".json"
				if os.path.exists(cachefile):
					with open(cachefile, 'r') as fh:
						geocode_result = json.loads(fh.read())
						fh.close()
				else:
					# Geocoding an address
					try:
						geocode_result = gmaps.geocode(row[0])
					except googlemaps.exceptions.HTTPError as error:
						print ('Failed to process "' + row[0] + '" due to ' + str(error))
						raise error
					with open(cachefile, 'w') as outfile:
						json.dump(geocode_result, outfile)
				geometry=None		
				if len(geocode_result) > 1:
					print ("More than one result for " + row[0])
					UKPlaces = []
					for result in geocode_result:
						for address in result["address_components"]:
							if address["short_name"] == "GB":
								UKPlaces.append(result)
					if len(UKPlaces) == 1:			
						geometry=UKPlaces[0]["geometry"]["location"]
					else:		
						print ("Found more than 1 places in the UK ")
						print (UKPlaces)
				elif len(geocode_result) == 0:
					print ("Failed to find " + row[0])
				else:	
					geometry=geocode_result[0]["geometry"]["location"]

				if geometry:	
					newrow.append(geometry["lng"])
					newrow.append(geometry["lat"])
				csvout.writerow(newrow)
