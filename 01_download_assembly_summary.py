#_*_coding:UTF-8_*_

"""
包含assembly_summary.txt的url地址列表
总的refseq信息，bacteria,archaea,fungi,viral,protozoa
"""

import subprocess
import argparse


def taxonomy():
    taxonomy_url = ["ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"]
    taxonomy_urls = ["ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz",
                     "ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz",
                     "ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz"]
    cmd0 = "mkdir taxonomy"
    subprocess.check_output(cmd0, shell=True)
    cmd1 = "cd taxonomy " + "&& " + "wget " + taxonomy_url[0]
    cmd2 = "cd taxonomy " + "&& " + " tar -zxvf " + taxonomy_url[0].split("/")[5]
    subprocess.check_output(cmd1, shell=True)
    subprocess.check_output(cmd2, shell=True)
    for url in taxonomy_urls:
        cmd3 = "cd taxonomy " + "&& " + "wget " + url
        cmd4 = "cd taxonomy " + "&& " + " gunzip " + url.split("/")[6]
        subprocess.check_output(cmd3, shell=True)
        subprocess.check_output(cmd4, shell=True)


def download_assembly():

    #ref seq genomes info download
    refseq_url = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/assembly_summary_refseq.txt"]
    refseq_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/refseq/bacteria/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/archaea/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/viral/assembly_summary.txt",
                       "ftp://ftp.ncbi.nih.gov/genomes/refseq/protozoa/assembly_summary.txt"]

    # genbank genomes info download
    genbank_url = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/assembly_summary_genbank.txt"]
    genbank_url_list = ["ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/archaea/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/fungi/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/viral/assembly_summary.txt",
                        "ftp://ftp.ncbi.nih.gov/genomes/genbank/protozoa/assembly_summary.txt"]

    # options "refseq"
    if args.input_type == "refseq":
        cmd = "wget -O " + refseq_url[0].split("/")[4] + "_" + refseq_url[0].split("/")[5] + " " + refseq_url[0]
        subprocess.check_output(cmd, shell=True)
        for ref_url in refseq_url_list:
            cmd1 = "wget -O " + ref_url.split("/")[4] + "_" + ref_url.split("/")[5] + "_" + ref_url.split("/")[6] + " " + ref_url
            subprocess.check_output(cmd1, shell=True)

    # options "genbank"
    elif args.input_type == "genbank":
        cmd = "wget -O " + genbank_url[0].split("/")[4] + "_" + genbank_url[0].split("/")[5] + " " + genbank_url[0]
        subprocess.check_output(cmd, shell=True)
        for genbank_url in genbank_url_list:
            cmd1 = "wget -O " + genbank_url.split("/")[4] + "_" + genbank_url.split("/")[5] + "_" + genbank_url.split("/")[6] + " " + genbank_url
            subprocess.check_output(cmd1, shell=True)

    # options "all"
    elif args.input_type == "all":
        # total info
        merger_url = []
        merger_url.append(refseq_url[0])
        merger_url.append(genbank_url[0])

        # split info
        merger_url_list = []
        for i in refseq_url_list:
            merger_url_list.append(i)
        for j in genbank_url_list:
            merger_url_list.append(j)
        for url in merger_url:
            cmd = "wget -O " + url.split("/")[4] + "_" + url.split("/")[5] + " " + url
            subprocess.check_output(cmd, shell=True)
        for url1 in merger_url_list:
            cmd1 = "wget -O " + url1.split("/")[4] + "_" + url1.split("/")[5] + "_" + url1.split("/")[6] + " " + url1
            subprocess.check_output(cmd1, shell=True)
    else:
        print("ERROR: CHECK THE TYPE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download assembly summary from genbank or refseq")
    parser.add_argument('-tax', "--taxonomy", type=str, help= "GenBank taxonomy files")
    parser.add_argument('-type',"--input_type",type=str, help="input the download directory such as 'refseq', 'genbank' or 'all'")
    args = parser.parse_args()
    if args.taxonomy == "taxonomy":
        taxonomy()
    elif args.input_type == "refseq" or args.input_type == "genbank" or args.input_type == "all":
        download_assembly()
    else:
        print("usage: download_assembly_summary_v1.py [-h] [-type INPUT_TYPE] [-tax TAXONOMY]")
