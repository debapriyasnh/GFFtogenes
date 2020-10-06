#! /usr/bin/env python
import argparse
import pybedtools
import pandas as pd
import csv
import os

def gfffile(file):
    track=pybedtools.BedTool(file)
    ref=pybedtools.BedTool('gencode.v28.annotation.gtf')
    gene = track.intersect(ref, wb=True)
    txtfile = gene.moveto('intersected.txt')
    df=pd.read_csv('intersected.txt', names=['ref1', 'source1', 'method1', 'start1', 'stop1', 'score1', 'strand1', 'phase1', 'group1', 'ref2', 'source2', 'feature', 'start2', 'stop2', 'score2','strand2', 'frame', 'attribute'], sep='\t')
    reqdf=df[['ref1','start1','stop1','score1','strand2','attribute']]
    reqdf.rename(columns={'ref1':'ref','start1':'start','stop1':'stop','score1':'score','strand2':'strand'}, inplace=True)
    return reqdf

#def bedfile(file):

#def bedgraphfile(file):


def run(args):
	global inputfile, outputfile, add
	inputfile = args.input # these match the "dest": dest="input"
	outputfile = args.output # from dest="output"
	name, extension = os.path.splitext(inputfile)
	print (extension)
	if (extension == ".gff"):
		reqdf = gfffile(inputfile)
	elif (extension == ".bedgraph"):
		reqdf = bedgraphfile(inputfile)
	elif (extension == ".bed"):
		reqdf = bedfile(inputfile)
	
	reqdf = reqdf[reqdf['attribute'].str.contains('gene_type "protein_coding"')]
	#split the string attribute into columns
	reqdf = reqdf.join(reqdf['attribute'].str.split(';', expand=True))
	reqdf = reqdf.drop('attribute', 1)
	#select the column that contains string "gene_name"
	selected_cols = list(range(0, 21))
	newdf=reqdf[reqdf[selected_cols].apply(lambda x: x.str.contains('gene_name'))]
	newdf[2].update(newdf.pop(3))
	newdf.isnull().sum()
	data = [reqdf["ref"], reqdf['start'], reqdf['stop'], newdf[2], reqdf['score'], reqdf['strand']]
	headers = ['ref','start','stop','name','score','strand']
	df3 = pd.concat(data, axis=1, keys=headers)
	df3 = df3.join(df3['name'].str.split('"', expand=True))
	df4 = [df3["ref"], df3['start'], df3['stop'], df3[1], df3['score'], df3['strand']]
	headers = ['ref','start','stop','name','score','strand']
	finaldf = pd.concat(df4, axis=1, keys=headers)
	finaldf.to_csv('output.bed', sep='\t', index=False)
	finaldf.to_csv('output.bed', sep='\t', quoting=csv.QUOTE_NONE, escapechar='"', index=False)
	combdf = finaldf.groupby(['name','score']).agg({'start':'min', 'stop':'max'}).reset_index()
	remdata = [finaldf["ref"], finaldf['name'], finaldf['strand']]
	headers = ['ref','name','strand']
	remcols = pd.concat(remdata, axis=1, keys=headers)
	remcols = remcols.drop_duplicates(subset='name', keep="first")
	finalcomb = pd.merge(combdf,remcols,how = "inner", on = "name")
	data = [finalcomb["ref"], finalcomb['start'], finalcomb['stop'], finalcomb['name'], finalcomb['score'], finalcomb['strand']]
	foroutput = pd.concat(data, axis=1)
	foroutput.head(20)
	foroutput = foroutput.rename(columns=foroutput.iloc[0]).drop(foroutput.index[0])
	foroutput.to_csv('afterfiltration.bed', sep='\t')
	foroutput.to_csv('afterfiltration.bed', sep='\t', quoting=csv.QUOTE_NONE, escapechar='"', index=False)
	a=pybedtools.BedTool('afterfiltration.bed').sort()
	a.moveto('afterfiltration_sorted.bed')

def main():
	global parser
	parser=argparse.ArgumentParser(description="Intersect bed/bedgraph/gff file to find non redundant information on genes")
	parser.add_argument("-in",help="input bed/bedgraph/gff file to intersect" ,dest="input", type=str, required=True)
	parser.add_argument("-out",help="fastq output filename" ,dest="output", type=str, required=False)
	parser.add_argument("-a",help="number to add" ,dest="toadd", type=int, default="0")
	parser.set_defaults(func=run)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()