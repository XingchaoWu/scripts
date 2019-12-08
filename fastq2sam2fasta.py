#_*_coding:UTF-8_*_

import os
import argparse
import subprocess

def fq2sam2fa(cur_path, bowtie2_path, samtools_path):
    # /home/pmd/analysis/PM19416/se_v1/R191129OTPN022/map/R191129OTPN022.non_human.exclude.fastq.gz
    bowtie2 = bowtie2_path + " -x " + args.index_path \
              + " -U /home/pmd/analysis/" + args.batch \
              +"/se_v1/" + args.sample + "/map/" + args.sample \
              + ".non_human.exclude.fastq.gz " + "--threads 12 --maxins 800 --end-to-end -S " \
              + cur_path + "/" + args.sample + ".sam" + " 2> " + cur_path + "/" + args.sample + ".sam.log"

    samtools_view = samtools_path + " view -bS " + args.sample + ".sam > " + args.sample + ".bam"
    samtools_fasta = samtools_path + " fasta -F 4 " + args.sample + ".bam > " + args.sample + ".mapped.fasta"

    subprocess.check_output(bowtie2, shell=True)
    subprocess.check_output(samtools_view, shell=True)
    subprocess.check_output(samtools_fasta, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("align and exclude mapped fasta")
    parser.add_argument("-I", "--index_path", type=str, help="bowtie2 index absolute path")
    parser.add_argument("-s", "--sample", type=str, help="sample number")
    parser.add_argument("-b", "--batch", type=str, help="batch")
    args = parser.parse_args()

    # /home/pmd/analysis/verification/PM19416
    cur_path = os.getcwd()
    bowtie2_path = "/opt/biotools/bowtie2-2.2.9/bowtie2"
    samtools_path = "/opt/apps/samtools-1.3/bin/samtools"
    fq2sam2fa(cur_path, bowtie2_path, samtools_path)