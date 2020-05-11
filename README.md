# IMPLICON
A processing guide for IMPLICON data (bisulfite amplicon data for imprinted loci)


[<img title="Babraham Bioinformatics" style="float:right;margin:20px 20 20 600px" id="Babraham Bioinformatics" src="Images/logo.png" height="88" >](http://www.bioinformatics.babraham.ac.uk/index.html)

Last update: 02/07/2019

#### Table of Contents
* [Quick Start](#quick-start)
* [Detailed Processing Guide](#detailed-processing-guide)
  1. [UMI-handling](#step-i-umi-handling)
  2. [Adapter-/Quality Trimming](#step-ii-adapter-quality-trimming)
  3. [Adapter Trimming](#step-iii-adapter-trimming)
    - [Auto-detection](#adapter-auto-detection)
    - [Manual adapter sequence specification](#manual-adapter-sequence-specification)
  3. [Removing Short Sequences](#step-3-removing-short-sequences)
  4. [Specialised Trimming - hard- and Epigenetic Clock Trimming](#step-4-specialised-trimming)
* [Full list of options for Trim Galore!](#full-list-of-options-for-trim-galore)
  * [RRBS-specific options](#rrbs-specific-options-mspi-digested-material)
  * [Paired-end specific options](#paired-end-specific-options)


## QUICK START

The following commands work with these hypothetical IMPLICON paired-end reads from a C57BL/6 mouse:
`test_R1.fastq.gz` and `test_R2.fastq.gz`.

**Step I: UMI-handling**

```
trim_galore --paired --implicon *fastq.gz
```

**Step II: Adapter-/quality trimming**

```
trim_galore --paired *UMI*fastq.gz
```

**Step III: Genome alignments**

```
bismark --genome /Genomes/Mouse/GRCm38/ -1 test_8bp_UMI_R1_val_1.fq.gz -2 test_8bp_UMI_R2_val_2.fq.gz
```

STEP IV: UMI-aware deduplication

```
deduplicate_bismark --barcode test_8bp_UMI_R1_val_1_bismark_bt2_pe.bam
```

STEP V: Methylation extraction

```
bismark_methylation_extractor --bedGraph --gzip test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.bam
```

6. 

## Detailed Processing Guide

### Step I: UMI handling

At its 5’ end, Read 2 carries 8 bp of randomised nucleotides that serve as unique molecular identifiers (UMI) for the amplification reaction. The UMI sequence needs to be transferred from the start of Read 2 to the readID of both reads to allow UMI-aware deduplication later, a step that can be accomplished using the Trim Galore with the option --implicon (for more information type trim_galore --help). In this step, the UMI of Read 2 is added to the readID of both reads as the last element separated by a “:”, e.g.:

@HWI-D00436:407:CCAETANXX:1:1101:4105:1905 1:N:0: CGATGTTT:CAATTTTG

To run this specialised UMI-transfer trimming on all files of a MiSeq run you can run this command:

```
trim_galore --paired --implicon *fastq.gz
```

Step I: UMI handling

At its 5’ end, Read 2 carries 8 bp of randomised nucleotides that serve as unique molecular identifiers (UMI) for the amplification reaction. The UMI sequence needs to be transferred from the start of Read 2 to the readID of both reads to allow UMI-aware deduplication later, a step that can be accomplished using the Trim Galore with the option --implicon (for more information type trim_galore --help). In this step, the UMI of Read 2 is added to the readID of both reads as the last element separated by a “:”, e.g.:

@HWI-D00436:407:CCAETANXX:1:1101:4105:1905 1:N:0: CGATGTTT:CAATTTTG

To run this specialised UMI-transfer trimming on all files of a MiSeq run you can run this command:

trim_galore --paired --implicon *fastq.gz

The FastQC per base sequence content plot would look something like this:

Read 2 - Raw FastQ file	Read 2 - after UMI handling
 	 


As an example, the following commands are exemplified by a set of test files:
 
Input files:
test_R1.fastq.gz
test_R2.fastq.gz

Output files:
test_8bp_UMI_R1.fastq.gz
test_8bp_UMI_R2.fastq.gz

### Step II: Adapter-/quality trimming

Following UMI-handling, IMPLICON reads require adapter and quality trimming. A standard Trim Galore run should identify and remove read-through adapter contamination as well as poor quality base calls, like so:

trim_galore --paired *UMI*fastq.gz

Output files:
test_8bp_UMI_R1_val_1.fq.gz
test_8bp_UMI_R2_val_2.fq.gz


Step III: Genome alignments

Alignments to the mouse or human genome can then be obtained with a standard Bismark run, e.g.:

bismark --genome /Genomes/Mouse/GRCm38/ -1 test_8bp_UMI_R1_val_1.fq.gz -2 test_8bp_UMI_R2_val_2.fq.gz

Relevant output files:
test_8bp_UMI_R1_val_1_bismark_bt2_pe.bam

The output BAM file is then ready for a UMI-aware deduplication step. 

Step IV: UMI-aware deduplication

In this step, paired-end read alignments are deduplicated based on:
•	chromosome
•	start position
•	end position
•	alignment orientation
•	UMI from the read header (see Step I)

deduplicate_bismark --barcode test_8bp_UMI_R1_val_1_bismark_bt2_pe.bam

Relevant output files:
test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.bam

Step V: Methylation extraction

Askjkhdjfh

bismark_methylation_extractor --bedGraph --gzip test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.bam

Relevant output files:

General methylation analysis (coverage file):
test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.bismark.cov.gz

CpG context files for bisulfite consistency analysis:
CpG_OB_test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.txt.gz (top strand)
CpG_OT_test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.txt.gz (bottom strand)
Step VI: Genome alignments

Askjkhdjfh

