#_*_coding:UTF-8_*_

import argparse
import subprocess
import os

def download_genome(cur_path,url_lists):
    # ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/803/615/GCA_001803615.1_ASM180361v1/GCA_001803615.1_ASM180361v1_genomic.fna.gz
    with open(args.input_file,"r") as in_file:
        for line in in_file:
            line = line.strip().split("\t")[19]
            url_lists.append(line)

    cmd0 = "mkdir " + args.type + " && " + "cd " + args.type
    subprocess.check_output(cmd0, shell=True)

    for url in url_lists:
        # cmd =  # 下载
        pass




def main():
    cur_path = os.getcwd()
    url_lists = []
    download_genome(cur_path,url_lists)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("download genome")
    parser.add_argument("-t", "--type", type=str, help="the taxonomy of genome, for example 'bacteria','fungi','viral','protozoa'")
    parser.add_argument("-i","-input_file",type=str,help="assembly_summary.txt, absolute file path")
    args = parser.parse_args()
    main()