# GFFtogenes
This is a script written to accurately convert peak regions in a gff formatted peak output into corresponding protein-coding genes. 
This tool provides the genes, corresponding peak score as well as the relative genomic region associated with the peak.
The basic structure of this tool is to use bedtools in order to intersect peak output with an annotated reference file (for example, "gencode.v28.annotation.gtf" as provided with the workflow). An example input is also provided.
