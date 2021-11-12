from __future__ import division
import sys, os, re
import fileutils as fl
from glob import glob

def EEnum(strNum):
	strNum = strNum.replace(" ", "")
	strNum = strNum.replace(",", "")
	return int(strNum)


def writeToFile(metadata, outLoc):
	PROCESSED_DATA = []
	GeneName = metadata[0]
	chromosome = ''
	if len(metadata[1].split('p')) > 1:
		chromosome = metadata[1].split('p')[0]
	elif len(metadata[1].split('q')) > 1:
		chromosome = metadata[1].split('q')[0]
	else:
		chromosome = 'NA'

	geneStartPos = EEnum(metadata[2].split('-')[0])
	for i, line in enumerate(metadata[3]):
		ExonNo = i+1
		startPos = geneStartPos + EEnum(line.split('-')[0])
		endPos = geneStartPos + EEnum(line.split('-')[1])
		PROCESSED_DATA.append([GeneName,chromosome,ExonNo,startPos,endPos])

	#Writing to file
	with open(outLoc, 'a') as f:
		for line in PROCESSED_DATA:
			for elem in line:
				f.write(str(elem)+',')
			f.write('\n')


def processFiles(geneList, outputfile):
	print("Processing Genes:", geneList)
	HEADER = ['GeneName', 'Chromosome', 'ExonNo', 'StartPos', 'EndPos']
	with open(outputfile, 'w') as f:
		for elem in HEADER:
			f.write(str(elem)+',')
		f.write('\n')

	for gene in geneList:
		#Opening file
		#try:
		if True:
			data = fl.readLines(os.path.join('.scrape.dump', str(gene)+'.p'))
			chr_location = data[10].split('>')[1].split('<')[0]
			gene_pos = data[12].split('>')[1].split('<')[0]
			
			EXONS = []
			for i, line in enumerate(data):
				if line.split('>')[0] == '<td class="aligned-right style-scope exons-mapping-table"':
					if len(line.split('>')[1].split('<')[0].split('-')) > 1:
						EXONS.append(line.split('>')[1].split('<')[0])
		HOLDER = [gene, chr_location, gene_pos, EXONS]
		writeToFile(HOLDER, outputfile)
		print("Successfully written Exon data for:", gene)
		#except:
		#	print(gene, "No datafile found")
