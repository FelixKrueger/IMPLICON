# IMPLICON
A processing guide for IMPLICON data (bisulfite amplicon data for imprinted loci)


[<img title="Babraham Bioinformatics" style="float:right;margin:20px 20 20 600px" id="Babraham Bioinformatics" src="Images/logo.png" height="88" >](http://www.bioinformatics.babraham.ac.uk/index.html)

Last update: 02/07/2019

#### Table of Contents
* [Introduction](#version-064)
* [UMI-handling](#step-i-umi-handling)
  1. [Quality Trimming](#step-1-quality-trimming)
  2. [Adapter Trimming](#step-2-adapter-trimming)
    - [Auto-detection](#adapter-auto-detection)
    - [Manual adapter sequence specification](#manual-adapter-sequence-specification)
  3. [Removing Short Sequences](#step-3-removing-short-sequences)
  4. [Specialised Trimming - hard- and Epigenetic Clock Trimming](#step-4-specialised-trimming)
* [Full list of options for Trim Galore!](#full-list-of-options-for-trim-galore)
  * [RRBS-specific options](#rrbs-specific-options-mspi-digested-material)
  * [Paired-end specific options](#paired-end-specific-options)


## QUICK START

1. UMI-handling

```
trim_galore --paired --implicon *fastq.gz
```

2. Adapter-/quality trimming

```
trim_galore --paired *UMI*fastq.gz
```

3. Genome alignments

```
bismark --genome /Genomes/Mouse/GRCm38/ -1 test_8bp_UMI_R1_val_1.fq.gz -2 test_8bp_UMI_R2_val_2.fq.gz
```

4. UMI-aware deduplication

```
deduplicate_bismark --barcode test_8bp_UMI_R1_val_1_bismark_bt2_pe.bam
```

5. Methylation extraction

```
bismark_methylation_extractor --bedGraph --gzip test_8bp_UMI_R1_val_1_bismark_bt2_pe.deduplicated.bam
```

6. 


### Step I: UMI handling

At its 5’ end, Read 2 carries 8 bp of randomised nucleotides that serve as unique molecular identifiers (UMI) for the amplification reaction. The UMI sequence needs to be transferred from the start of Read 2 to the readID of both reads to allow UMI-aware deduplication later, a step that can be accomplished using the Trim Galore with the option --implicon (for more information type trim_galore --help). In this step, the UMI of Read 2 is added to the readID of both reads as the last element separated by a “:”, e.g.:

@HWI-D00436:407:CCAETANXX:1:1101:4105:1905 1:N:0: CGATGTTT:CAATTTTG

To run this specialised UMI-transfer trimming on all files of a MiSeq run you can run this command:

```
trim_galore --paired --implicon *fastq.gz
```
