#!/usr/bin/python -u

import json
from lxml import etree
from lxml.builder import ElementMaker

namespaces = {
	"mil":"http://rdf.muninn-project.org/ontologies/military#",
	"bor":"http://data.llgc.org.uk/bor/def#",
	"waw":"http://data.llgc.org.uk/waw/def#",
	"mil":"http://rdf.muninn-project.org/ontologies/military#",
	"foaf":"http://xmlns.com/foaf/0.1/",
	"rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	"rdfs":"http://www.w3.org/2000/01/rdf-schema#" 
}
def xpath(dom, path):
	return dom.xpath(path, namespaces=namespaces)

	
with open('solr.json', 'r') as f:
    solr = json.load(f)

root = etree.Element("{"+ namespaces["rdf"] + "}RDF", nsmap=namespaces)
count=0
for response in solr["response"]["docs"]:
	if 'within' in response.keys() and response["within"][0] == 'http://dams.llgc.org.uk/iiif/2.0/4642022/manifest.json':
		if 'body' in response.keys():
			if len(response["body"]) > 1:
				print ("text " + str(response["body"]))
			else:
				count += 1
				try:
					data = etree.XML("<root>" + response["body"][0].replace("&nbsp;"," ") + "</root>")
					print (etree.tostring(data, pretty_print = True))

					desc = etree.SubElement(root, "{" + namespaces["rdf"] + "}Description")

					desc.set("{" + namespaces["rdf"] + "}about", response["id"])

					if xpath(data,"//span[@property='ns:rank']"):
						rank = etree.SubElement(desc, "{" + namespaces["mil"] + "}heldRank")
						rank.text = xpath(data,"//span[@property='ns:rank']")[0].text
					if xpath(data,"//span[@property='ns:name']"):
						el = etree.SubElement(desc, "{" + namespaces["rdfs"] + "}label")
						el.text = xpath(data,"//span[@property='ns:name']")[0].text
					if xpath(data,"//span[@property='ns:place']"):
						el = etree.SubElement(desc, "{" + namespaces["foaf"] + "}based_near")
						el.text = xpath(data,"//span[@property='ns:place']")[0].text

					if xpath(data,"//span[@property='ns:unit']"):
						el = etree.SubElement(desc, "{" + namespaces["bor"] + "}servedInUnit")
						el.text = xpath(data,"//span[@property='ns:unit']")[0].text
					if xpath(data,"//span[@property='ns:ship']"):
						el = etree.SubElement(desc, "{" + namespaces["bor"] + "}servedOnShip")
						el.text = xpath(data,"//span[@property='ns:ship']")[0].text
					if xpath(data,"//span[@property='ns:medal']"):
						el = etree.SubElement(desc, "{" + namespaces["waw"] + "}awarded")
						el.text = xpath(data,"//span[@property='ns:medal']")[0].text
				except etree.XMLSyntaxError as issue:
					print ('failed to parse:')
					print (response["body"][0])
					print (issue)
		else:
			print ('failed to process ' + response["id"])

print ("total found " + str(count))			
#print ("RDF: " + etree.tostring(root, pretty_print = True))
tree = etree.ElementTree(root)
tree.write('bor_ann.rdf',encoding="UTF-8",xml_declaration=True, pretty_print = True)
