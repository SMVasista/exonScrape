from __future__ import division
import sys, os, re, random, pickle
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep
from parsel import Selector

# function to ensure all key data fields have a value
def validate_field(field):# if field is present pass if field:pass
	if field != None:
		return field
	else:
		return 'NR'

def execute(urls):
	HOLDER = {}

	# Configuring Firefox driver (geckodriver)
	cwl = os.getcwd()
	driverpath = str(os.path.join(cwl, 'geckodriver'))
	cap = {"marionette": True}

	driver = webdriver.Firefox(capabilities = cap, executable_path=driverpath)

	for gene in urls.keys():
		#try:
		if True:
			# get the profile URL
			print(urls[gene])
			driver.get(urls[gene])

		   # add a 5 second pause loading each URL
			sleep(3 + random.randint(1, 4))

		   #Souping data
			html = unicode(driver.page_source.encode("utf-8"), "utf-8")
			data = soup(html, 'html.parser')
		   
		   #Extracting gene-start&end location
			Gdata = data.findAll("tr", {"class", "style-scope gene-information-section"})

			#Extracting exon locations
			LOCS = []
			EXData = data.findAll("td", {"class", "aligned-right style-scope exons-mapping-table"})
			HOLDER[gene] = [Gdata, EXData]
			with open(os.path.join('.scrape.dump', str(gene)+'.p'), 'w') as f:
				for elem in Gdata:
					f.write(str(elem)+'\n')
				for elem in EXData:
					f.write(str(elem)+'\n')
		#except:
		#	print("issue extracting data for gene:", gene)
		#	pass
	driver.quit()
	return 1