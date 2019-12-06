# —*—coding:utf-8_*_
# 2019-11-30

import os
import argparse
import subprocess


def search_urls(urls,cur_path):
    file_path = args.dirctory + "/" + args.input_file
    line_num = 0
    with open (file_path, "r") as in_file:
        if line_num >=2:
            for line in in_file:
                line =line.strip().split("\t")  # Remove the leading and trailing Spaces and split the data with "\t"
                if line[6] == args.taxid:
                    urls.append(line[19])
                else:
                    pass
        else:
            line_num +=1
    in_file.close()
    storage_path = cur_path + "/" + args.out_file
    with open(storage_path,"w") as out_file:
        for url in urls:
            out_file.write(url + "\n")
    out_file.close()
    return urls

def download_genome(urls):
    # make new dirctory
    cmd_0 = "mkdir " + args.taxid + "_assembly_genome"
    subprocess.check_output(cmd_0, shell=True)
    # download genome
    for url in urls:
        cmd_1 = "wget -P " + args.taxid + "_assembly_genome "+ url + "/" + url.split("/")[-1] + "_genomic.fna.gz"
        subprocess.check_output(cmd_1, shell=True)
        print(args.taxid + " genome download complete")
    # gunzip
    cmd_2 = "gunzip *"
    subprocess.check_output(cmd_2, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download the genome according to taxid from NCBI")
    parser.add_argument("-t", "--taxid", type=str, help="taxid '9606' ")
    parser.add_argument("-d", "--dirctory", type=str, help="file storage path")
    parser.add_argument("-i", "--input_file", type=str, help="file name: 'assembly_summary.txt'")
    parser.add_argument("-o", "--out_file", type=str, help="file name: *_out.txt")
    args = parser.parse_args()
    cur_path = os.getcwd()
    urls = []
    search_urls(urls,cur_path)