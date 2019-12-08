#_*_coding:UTF-8_*_
# 2019-11-30

import os
import argparse
import subprocess
from pathlib2 import Path


def search_urls(urls,cur_path):
    file_path = args.dirctory + "/" + args.input_file
    line_num = 0
    with open (file_path, "r") as in_file:
        for line in in_file:
            if line_num >= 2:
                line =line.strip().split("\t")  # Remove the leading and trailing Spaces and split the data with "\t"
                if line[6] == args.taxid:
                    urls.append(line[19])
                else:
                    continue
            else:
                line_num +=1
    # make new dirctory
    target_file = Path(cur_path + "/" + args.taxid + "_assembly_genome")
    if target_file.exists():
        storage_path = cur_path + "/" + args.taxid + "_assembly_genome" + "/" + args.taxid + "_download_url.txt"
        with open(storage_path,"w") as out_file:
            for url in urls:
                out_file.write(url + "/" + url.split("/")[-1] + "_genomic.fna.gz" + "\n")
    else:
        cmd_0 = "mkdir " + args.taxid + "_assembly_genome"
        subprocess.check_output(cmd_0, shell=True)
        storage_path = cur_path + "/" + args.taxid + "_assembly_genome" + "/" + args.taxid + "_download_url.txt"
        with open(storage_path, "w") as out_file:
            for url in urls:
                out_file.write(url + "/" + url.split("/")[-1] + "_genomic.fna.gz" + "\n")
    in_file.close()
    out_file.close()
    return urls


def download_genome(urls):
    # download genome
    for url in urls:
        cmd_1 = "wget -P " + cur_path + "/" + args.taxid + "_assembly_genome "+ url + "/" + url.split("/")[-1] + "_genomic.fna.gz"
        subprocess.check_output(cmd_1, shell=True)
        # formate fasta
        print(args.taxid + " genome download complete")

    # gunzip
    cmd_2 = "cd " + cur_path + "/" + args.taxid + "_assembly_genome" +" && "+ "gunzip *.gz"
    subprocess.check_output(cmd_2, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download the genome according to taxid from NCBI")
    parser.add_argument("-t", "--taxid", type=str, help="taxid '9606' ")
    parser.add_argument("-d", "--dirctory", type=str, help="file storage path")
    parser.add_argument("-i", "--input_file", type=str, help="file name: 'assembly_summary.txt'")
    args = parser.parse_args()
    cur_path = os.getcwd()
    urls = []
    search_urls(urls,cur_path)
    download_genome(urls)