# IMPLICON
A processing guide for IMPLICON data (bisulfite amplicon data for imprinted loci)


[<img title="Babraham Bioinformatics" style="float:right;margin:20px 20 20 600px" id="Babraham Bioinformatics" src="Images/logo.png" height="88" >](http://www.bioinformatics.babraham.ac.uk/index.html)

Last update: 02/07/2019

#### Table of Contents
* [Introduction](#version-064)
* [UMI-handling](#step-1-umi-handling)
  1. [Quality Trimming](#step-1-quality-trimming)
  2. [Adapter Trimming](#step-2-adapter-trimming)
    - [Auto-detection](#adapter-auto-detection)
    - [Manual adapter sequence specification](#manual-adapter-sequence-specification)
  3. [Removing Short Sequences](#step-3-removing-short-sequences)
  4. [Specialised Trimming - hard- and Epigenetic Clock Trimming](#step-4-specialised-trimming)
* [Full list of options for Trim Galore!](#full-list-of-options-for-trim-galore)
  * [RRBS-specific options](#rrbs-specific-options-mspi-digested-material)
  * [Paired-end specific options](#paired-end-specific-options)


### Step I: UMI handling

At its 5’ end, Read 2 carries 8 bp of randomised nucleotides that serve as unique molecular identifiers (UMI) for the amplification reaction. The UMI sequence needs to be transferred from the start of Read 2 to the readID of both reads to allow UMI-aware deduplication later, a step that can be accomplished using the Trim Galore with the option --implicon (for more information type trim_galore --help). In this step, the UMI of Read 2 is added to the readID of both reads as the last element separated by a “:”, e.g.:

@HWI-D00436:407:CCAETANXX:1:1101:4105:1905 1:N:0: CGATGTTT:CAATTTTG

To run this specialised UMI-transfer trimming on all files of a MiSeq run you can run this command:

trim_galore --paired --implicon *fastq.gz

