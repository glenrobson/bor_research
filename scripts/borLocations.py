#!/usr/local/bin/python3 -u

import os
import json
from lxml import etree
from io import StringIO
from collections import Counter
import csv

if __name__ == "__main__":
    data=os.path.dirname(os.path.realpath(__file__)) + "/../data/annos"
    htmlparser = etree.HTMLParser()
    places = []
    for annoList in os.listdir(data):
        with open ("%s/%s" % (data,annoList), 'r') as fh:
            jsondata = json.load(fh)
            for anno in jsondata:
                content = anno["resource"][0]["chars"]
                if 'ns:place' in content:
                    try:
                        xml = etree.parse(StringIO(content), htmlparser)
                        #xml = etree.XML("<p>" + content.replace("&nbsp;"," ") + "</p>")
                        place = xml.xpath("//span[@property='ns:place']")[0].text
                        if place and place.strip():
                            places.append(place.strip())
                        print ("found place %s" % place)
                    except Exception as e:
                        print ('Failed to read "%s"' % content)
                        print (e)
                        sys.exit(-1)


    placeCount = Counter(places)
    with open('../bor_places.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        d_view=[]
        for key in placeCount:
            value  = placeCount[key]
            if not value:
                value=0
            if not key:
                key='missing'
            d_view.append((value, key))
        print(d_view)
        d_view.sort(reverse=True) # natively sort tuples by first element
        for place,count in d_view:
            print ('place %s count %s' % (place, count))
            csvwriter.writerow([ place , count])
