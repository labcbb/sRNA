#! /user/bin/env bash

/data/home/leijiaxin2/miniconda3/envs/chipseq/bin/cutadapt -a AACTGTAGGCAC -m 15 -j 8  --trim-n  /data/home/leijiaxin2/mrna/Pancreaticcancer/SRP425933/SRP425933-sample/SRR23717242.fastq.gz -o /data/home/leijiaxin2/mrna/Pancreaticcancer/SRP425933/SRP425933-sample/SRR23717242_trimmed.fastq.gz
