# GFFtogenes
This is a script written to accurately convert peak regions in a gff formatted peak output into corresponding protein-coding genes. 
This tool provides the genes, corresponding peak score as well as the relative genomic region associated with the peak.
The basic structure of this tool is to use bedtools in order to intersect peak output with an annotated reference file (for example, "gencode.v28.annotation.gtf"). An example input is provided.
After intersecting with the annotated reference, the output is parsed and a final output is produced in a bed-format. Bedtools is again used to sort the final output.


The GFF_to_genes.py can be run via command line with the following code:

python GFF_to_genes.py -in [path to input file]

This tool creates 4 files in the directory in which it is run:
1. intersected.txt : the first file after intersection of the input gff/bedgraph/bed file with the annotated reference
2. output.bed: the first processed file that consists of columns reference, start, stop, name, score, strand. This file may contain multiple repeats of the gene names and multiple overlapping start and stop sites.
3. afterfiltration.bed: this is a bed file consisting of reference, start, stop, gene-name, score, strand columns. It does not possess multiple overlapping sites of each gene. May possess duplicate genes, but the start-stop and corresponding scores should be different.
4. afterfiltration_sorted.bed: bedtools sort function has been used to sort the afterfiltration.bed file.
