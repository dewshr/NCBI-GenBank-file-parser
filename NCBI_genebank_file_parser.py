#@Dewan Shrestha

from Bio import GenBank

#reading the gene bank file
def readfile():
	#for genbank file: ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh37_latest/refseq_identifiers/
	gb_file_name = str(raw_input("Enter your NCBI gene bank file name: "))
	
	try:
		genbank = open(gb_file_name).read().split('LOCUS  ') #opens gene bank file and splits by '//\n' to create list of each genes
	except:
		print "File not found. Please make sure you have the right file and also include the file extension"

	return genbank


#function to parse the nucleotide reference sequence genebank file
def ntgenbank():
	#retreiving all genebank files in a list calling another function
	nuc_genbank = readfile()
	#nuc_genbank = filter(None, nuc_genbank)
	print len(nuc_genbank)
	print nuc_genbank[0]
	length = len(nuc_genbank) #since last element is new line, total length will be total length of list -1
	print "\nParsing started"
	output = open('result_ntgenbank.csv','w') # opening a file to write the ouput

	#writing headings of the output file
	output.write('Name'+','+'NM'+','+ 'NM_version'+','+ 'Symbol'+','+'CDS_start'+','+ 'CDS_stop'+','+'HGNC'+','+\
		    'MIM'+','+'EC_number'+','+ 'GeneID' +','+ 'NP'+','+'NP_version'+','+'gene_synonym'+','+'AA_seq'+','+\
		     'AA_number'+','+'Chromosome'+ ','+'Chromosome_map'+','+ 'NT_seq'+','+'Organism'+'\n')
	
	# going through all the genes in the list
	for n in range(1,length):
		print n
		test= 'LOCUS  ' + nuc_genbank[n].lstrip('\n')   #removing new line of from individual genebank files
		query = open('genbank.txt','w')	#creating a genbank file to create query gene bank file
		query.write(test)
		query.close()
		parser = GenBank.RecordParser()		#using biopython function for parsing
		record = parser.parse(open('genbank.txt'))
		

		##########################################################################################
		nt_seq = (record.sequence).strip('\n') #stores nucleotide sequence
		nm_and_version = (record.version).strip('\n') #contains nm and nm_version
		nm = (nm_and_version.split('.')[0]).strip('\n')
		nm_version = (nm_and_version.split('.')[1]).strip('\n')


		############################################################################################
		source = record.features[0]			#contains all the fields of source
		organism = source.qualifiers[0].value.strip('\n')+ ':'+source.qualifiers[2].value.strip('\n')
		try:
			organism = source.qualifiers[0].value.strip('\n')+ ':'+source.qualifiers[2].value.strip('\n')
		except:
			organism =''
		
		try:
			chrm = (source.qualifiers[3].value).strip('\n') #stores chromosome number
		except:
			chrm = ''
			
		try:
			chrm_map = source.qualifiers[4].value.strip('\n')
		except:
			chrm_map = ''
                        

		############################################################################################
		gene = record.features[1]			#contains all the field of gene
		symbol = (gene.qualifiers[0].value).strip('\n')     #symbol or gene


                #########################################################################################
		cds=''		
		for c in range(0, len(record.features)):
			if('CDS' in record.features[c].key):
				cds = record.features[c]
				break
			else:
				continue

		if cds != '':
			
			cds_start_stop = (cds.location).strip('\n')		#stores cds start and stop position
			cds_start = (cds_start_stop.split('..')[0]).strip('\n')
			cds_stop = (cds_start_stop.split('..')[1]).strip('\n')
			

			#creating a empty dictionary to go through the elements in the CDS and update later if present
			cds_dict = {"HGNC":'', "MIM:":'', "EC_number":'', "GeneID":'', "product":'', 
					"protein_id":'',"translation":'',"num_aa":'', "gene_synonym":''}

			for n in range(0, len(cds.qualifiers)):		#going through all the elements in the cds
				for key, value in cds_dict.iteritems():	#looping through the dictionary items to see if present in cds
					if ((key in cds.qualifiers[n].key) or (key in cds.qualifiers[n].value)):
						keys =str(key)					#storing dictionary key
						cds_dict[keys] = str(cds.qualifiers[n].value) #updating dictionary key with values
						break
					else:
						continue
			np = cds_dict["protein_id"].split('.')[0]+'"'
			np_version = '"'+cds_dict["protein_id"].split('.')[1]
			hgnc=cds_dict["HGNC"]
			mim=cds_dict["MIM:"]
			geneid =cds_dict["GeneID"]
			name = cds_dict["product"]
			synonym = cds_dict["gene_synonym"]
			translation = cds_dict["translation"]
			if translation != '': num_aa = len(translation)
			if len(hgnc) !=0:
				hgnc = '"'+hgnc.split(':')[2]
			if len(mim) !=0:
				mim = '"'+mim.split(':')[1]
			if len(geneid) !=0:
				geneid = '"'+geneid.split(':')[1]

			gvalue = name+','+nm+','+nm_version+','+symbol+','+cds_start+','+cds_stop+',' + hgnc +','+\
				mim+','+cds_dict["EC_number"]+','+geneid+ ','+np+','+np_version+','+synonym+','+\
				translation+','+str(num_aa) +','+str(chrm)+','+chrm_map+','+nt_seq+','+organism+'\n'
			output.write(gvalue)
	print "Parsing completed"
	output.close()
	
ntgenbank()
