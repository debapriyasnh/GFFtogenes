# GFFtogenes
This is a script written to accurately convert peak regions in a gff formatted peak output into corresponding protein-coding genes. 
This tool provides the genes, corresponding peak score as well as the relative genomic region associated with the peak.
The basic structure of this tool is to use bedtools in order to intersect peak output with an annotated reference file (for example, "gencode.v28.annotation.gtf"). An example input is provided.
After intersecting with the annotated reference, the output is parsed and a final output is produced in a bed-format. Bedtools is again used to sort the final output.


Ongoing work is to convert the script into an object oriented program to make it easily executable.
