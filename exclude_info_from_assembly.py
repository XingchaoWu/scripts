# _*_coding=UTF-8_*_

import subprocess
import argparse

# ref seq genomes info download
# refseq_url = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/assembly_summary_refseq.txt"]
# refseq_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/bacteria/assembly_summary.txt",
#                    "ftp://ftp.ncbi.nih.gov/genomes/refseq/archaea/assembly_summary.txt",
#                    "ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/assembly_summary.txt",
#                    "ftp://ftp.ncbi.nih.gov/genomes/refseq/viral/assembly_summary.txt",
#                    "ftp://ftp.ncbi.nih.gov/genomes/refseq/protozoa/assembly_summary.txt"]
# genbank genomes info download
# genbank_url = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/assembly_summary_genbank.txt"]
# genbank_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt",
#                     "ftp://ftp.ncbi.nih.gov/genomes/genbank/archaea/assembly_summary.txt",
#                     "ftp://ftp.ncbi.nih.gov/genomes/genbank/fungi/assembly_summary.txt",
#                     "ftp://ftp.ncbi.nih.gov/genomes/genbank/viral/assembly_summary.txt",
#                     "ftp://ftp.ncbi.nih.gov/genomes/genbank/protozoa/assembly_summary.txt"]

types = ["bacteria", "fungi", "viral", "protozoa"]

# url = "ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt"
url = "ftp://ftp.ncbi.nih.gov/genomes/*/*/assembly_summary.txt"
# 读取genbank_
def read_genbank_assembly_summary():
    # cmd = ("cat genbank_%s_assembly_summary.txt " + "awk -F '\t' '{print$1}' > genbank_%s_assembly_summary_exclude.txt")%(type,type)
    # subprocess.check_output(cmd, shell=True)

def read_refseq_assembly_summary():
    pass


def merge_assembly_summary():
    pass





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument()