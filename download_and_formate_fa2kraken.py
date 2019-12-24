#_*_coding:UTF-8_*_
import os
import argparse
import subprocess


def obtain_ftp(ftp_dict):
    # exclude ftp
    with open(args.assembly_genbank,"r") as gene_bank:
        for line in gene_bank:
            if not line.startswith("#"):
                line = line.strip().split("\t")
                ftp_dict[line[0]] = [line[5],line[19]]

def download_formate2kraken(ftp_dict,cur_path):
    for k in ftp_dict.keys():
        if k == args.accession:
            ftp = ftp_dict[k][1]

            # download genome
            download_genome = "wget " + ftp + "/" + ftp.split("/")[-1] + "_genomic.fna.gz"
            subprocess.check_output(download_genome, shell=True)
            # gunzip genome
            gunzip_file = "gunzip " + ftp.split("/")[-1] + "_genomic.fna.gz"
            subprocess.check_output(gunzip_file,shell=True)

            # formate_fa
            with open(cur_path + "/" + ftp.split("/")[-1] + "_genomic.fna", "r") as in_fa:
                with open(cur_path + "/" + ftp.split("/")[-1] + "_genomic_kraken.fna", "w") as out_fa:
                    for line in in_fa:
                        if line.startswith(">"):
                            out_fa.write(line.strip().split(" ")[0] + "|kraken:taxid|" + ftp_dict[k][0] + "\n")
                        else:
                            out_fa.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Accession to download the genome and format as kraken")
    parser.add_argument("-ac","--accession",type=str,help="accession num")
    parser.add_argument("-as","--assembly_genbank", type=str,help="assembly_summary_genbank.txt")
    args = parser.parse_args()
    ftp_dict = {}
    cur_path = os.getcwd()
    obtain_ftp(ftp_dict)
    download_formate2kraken(ftp_dict,cur_path)