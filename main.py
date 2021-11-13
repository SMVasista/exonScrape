from __future__ import division
import sys, os, re
import scrape as sc
import curate as cr
import fileutils as fl
from glob import glob

def loadGeneQueries(fileloc):
	#Reading gene IDs and converting to NX Ids
	try:
	#if True:
		nxid = fl.readLinesAndSplit('.gene_nxid_map.txt', ',')
		MAP = {}
		for line in nxid:
			MAP[line[0]] = line[1]

		url_base = 'https://www.nextprot.org/entry/'
		url_end = "/exons"
	except:
		print("NXIDs file not found")
		exit(1)

	gene_data = fl.readLines(fileloc)

	#Checking if dump data already present
	fileList = glob(os.path.join('.scrape.dump', '*'))
	GFlist = []
	for fil in fileList:
		GFlist.append(os.path.basename(fil).split('.')[0])

	intersection = list(set(gene_data).intersection(set(GFlist)))
	finalScrapeList = []

	for gene in gene_data:
		if gene not in intersection:
			finalScrapeList.append(gene)
	print(str(len(finalScrapeList)), "new genes to be scraped")


	URLS = {}
	for gene in finalScrapeList:
		if gene in MAP.keys():
			URLS[gene] = url_base+str(MAP[gene])+url_end
		else:
			pass

	return gene_data, URLS

def scrapeData(urls):
	signal = sc.execute(urls)
	return signal


if __name__=="__main__":
	script, genelist, outputfile = sys.argv
	gene_data, urls = loadGeneQueries(genelist)
	if len(urls.keys()) > 0:
		signal = scrapeData(urls)
	cr.processFiles(gene_data, outputfile)
