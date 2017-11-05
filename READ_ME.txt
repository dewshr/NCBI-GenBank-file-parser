############################# About the program ################################

This program takes the NCBI nucletotide gene bank file and then parses the information present in NCBI gene bank file to create a .csv file with each fields in one column. You can provide any file extension but the format of the file has to be similar to .gbff file. One example file is also provided as an example file. Running the program will ask for the file name, and while giving the file name, extension of the file has to be given too, the program assumes the file is present in the same location as of the program, if your file is present in another location then you can change the source script to give the location or you can just copy the script in the file location.

You can provide a file with single genbank entry or multiple entries. After running the program this will also create a txt file called 'genbank.txt', you can delete this file.
NOTE: this program will only give output to the gene bank files with CDS features. The fields for certain columns may be empty if respective information is not present in the genbank file.


############################# Program Requirements ###################################################
- installation of Biopython
- python 2.7

#################################### NCBI gene bank file link #########################################
ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/

