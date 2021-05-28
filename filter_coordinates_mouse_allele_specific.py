#!/usr/bin/env python
import sys, gzip, os
import getopt
from glob import glob
from time import sleep
import timeit
import re

'''
This script was last changed on May 28, 2021 
'''

cpg_positions = {} # storing all relevant CpG positions for the amplicon experiment
genes = {}         # the total number of possible CpG positions per gene

# moving this out to be global variable so that reads IDs are unique
reads_processed = 0

def main():
	
	print (f"Python version: {sys.version}.")
	print (f"Reading in amplicons from file supplied as '{sys.argv[1]}'")	
	
	# get imprinted CpG positions
	read_annotation()
	 
	bismark_files = glob("CpG_*.txt.gz")
	print (f"Analysing the following Bismark CpG files:\n{bismark_files}")

	outfile = 'methylation_state_consistency.txt'
	outfh  = open (outfile,"w")

	repeat_vals = [f"{i}" for i in range(1,32)]

	# Creating a header line with 31 positional values so that we can read it into R more easily
	outfh.write ("\t".join(["readID","sample","allele","implicon"])+ "\t" + "\t".join(repeat_vals) + "\n")

	for cpg_file in bismark_files:
		read_bismark_cpg_file(cpg_file,outfh)

	outfh.close()
	print (f"All done. Final number of reads processed: {reads_processed}\n")

def read_bismark_cpg_file(cfile,outfh):
	
	print (f"Reading file: >{cfile}<")
	
	global reads_processed

	with gzip.open(cfile) as cf:
				
		read = {}   # dictionary storing one full read and its covered positions
		old_readID = ''
		
		for line in cf:
			# discarding optional header
			if line.decode().startswith("Bismark"): 
				# print (f"First line: >>{line.decode().strip()}<<. Skipping...")
				continue

			readID,state,chrom,pos = [ line.decode().strip().split(sep="\t")[i] for i in [0,1,2,3]]
			pos = int(pos)
			# print(f"ID: {readID}\tState: {state}\tChromosome: {chrom}\tPos: {pos}")
			# sleep(1)
			if chrom in cpg_positions:
				
				if pos in cpg_positions[chrom]:	
					# print (f"Found it! ID: {readID}\tPos: {pos}\tGene: {cpg_positions[chrom][pos]}")
					
					if old_readID == '': # first readID
					    # print (f"Setting old_readID to {readID}")
						old_readID = readID
						read['ID'] = readID
						read['gene'] = cpg_positions[chrom][pos]
						read['filename']  = cfile
						read['positions'] = {}

					if old_readID == readID: # still the same read. Appending this position
						#' read['positions'].append(f"{state}:{pos}")
						read['positions'][pos] = state
					else:
						# print (f"Found new read.\nOld read ID: {old_readID}\nnew read ID: {readID}\nProcessing old read now.")
						reads_processed += 1
						process_read(read,outfh,reads_processed) # process entire Read to generate graphable output
						
						# print (f"Setting up new read")
						# Resetting read dictionary
						read.clear()
						# print ("clearing read dictionary")
						# sleep(1)
						# Setting up new read
						old_readID = readID
						read['ID'] = readID
						read['gene'] = cpg_positions[chrom][pos]
						read['filename']  = cfile
						read['positions'] = {}
						read['positions'][pos] = state
					
				else:
					continue # position is not of interest as position doesn't match known positions
			else:
				continue # position is not of interest as chromosome doesn't match known positions
		
		if read:
			process_read(read,outfh,reads_processed) # process entire Read to generate graphable output
			reads_processed += 1
	
	
	print (f"Finished processing file {cfile}. Amplicon reads processed in total: {reads_processed}\n###############\n")
	sleep(1)


def process_read(read, outfh, reads_processed):
	
	# print (f"Got following read {read}")
		
	# extracting useful parts from filename
	pattern = 'CpG_O._lane\d+_[TACG]{8}_(.*)_L00.*\.(genome[12])'
	# example read: 'CpG_OB_lane6808_TCTGCTGT_9C_A8_miPSC_L001_R1.UMI_val_1_CAST_EiJ_N-masked_GRCm38_bismark_bt2_pe.deduplicated.genome1.txt.gz'

	filename = read['filename']
	p = re.compile(pattern)
	# print (filename)
	m = p.findall(filename)
	sample = m[0][0]
	genome = m[0][1]
	
	if genome == 'genome1':
		allele = 'B6'
	elif genome == 'genome2':
		allele = 'CAST'
	else:
		sys.exit("Failed to extract allele")

	output = []
	output.append(reads_processed) # using a runnin read count instead of
	# output.append(read['ID'])    # this rather long readID to save space from the output file
	output.append(sample)
	output.append(allele)
	output.append(read['gene']) 
	#print (f"{read_positions['ID']}\t{sample}\t{allele}\t{read_positions['gene']}\t{genes[read_positions['gene']]}\t{len(read_positions['positions'])}",end="\t")
	
	methylation_states = []

	for implicon_pos in genes[read['gene']]:
		# print (f"{implicon_pos}")

		if implicon_pos in read['positions'].keys():
			# print (f"{implicon_pos} and {read['positions'][implicon_pos]}" )
			if read['positions'][implicon_pos] == '-':
				methylation_states.append(0)
			elif read['positions'][implicon_pos] == '+':
				methylation_states.append(1)
			else:
				sys.exit("Failed to get a sensible methylation state for this position")
		else:
			methylation_states.append("NA")
	
	# print (f"Methylation states: {methylation_states}")
	# joining the output
	output += methylation_states
	#  print ('\t'.join(map(str,output)))
	outfh.write('\t'.join(map(str,output)) + "\n")
		
	
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)	

def read_annotation():
	
	'''
	First we need to read in the positions of CpG within the amplicons
	'''
	
	with open(sys.argv[1]) as f:

		count = 0
		
		for line in f:
			if count == 0: # 
				# eprint (f"Skipping header line >{line.strip()}<")
				# sleep(1)
				count += 1
				continue

			count += 1
			# print (f"line {count}; content >{line.strip()}<")
			# sleep(1)

			name, chrom, pos, irr, gene  = line.strip().split("\t") # irr is irrelevant
			# print (f"\t\tGene: {gene}\tChromosome: {chrom}\tPosition: {pos}")
			pos = int(pos)
			if chrom in cpg_positions.keys():
				pass
				# print (f"already present: {chrom}")
			else:
				cpg_positions[chrom] = {}

			cpg_positions[chrom][pos] = gene

			if not gene in genes:
				genes[gene] = []
			
			genes[gene].append(pos)  # keeping track of the overall number of CpG achievable per amplicon

		# print ("All chromosomes:")
		# for ch, rest in cpg_positions.items():
		# 	print (ch)
		# 	for pos in cpg_positions[ch].keys():
		# 		# print (f"pos: {pos}\tgene: {gene}")
		# 		print (f"pos: {pos}\tgene: {cpg_positions[ch][pos]}")
		# 	 sleep(1)
	
	# print (f"Stored the following number of CpG positions per implicon:")
	# for g in genes:
	#  	print (f"{g}\t{genes[g]}")

	eprint ("Finished reading annotations\n")



if __name__ == "__main__":
	main()
else:
	print ("Just getting imported")
