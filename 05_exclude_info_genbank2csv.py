#_*_coding:UTF-8_*_

import os
import argparse
import subprocess
import csv

def exclude_gb_info(current_path):
    # 生成中间文件.tmp
    cmd0 = "grep -v '#' " + args.path + "/" + args.file + " > ./.tmp"
    subprocess.check_output(cmd0,shell=True)
    info_dicts ={}
    with open(current_path + "/" + ".tmp", "r") as f:
        for line in f:
            info_dicts[line.split("\t")[0]] = []
            info_dicts[line.split("\t")[0]].append(str(line.split("\t")[4]))
            info_dicts[line.split("\t")[0]].append(str(line.split("\t")[5]))
            info_dicts[line.split("\t")[0]].append(str(line.split("\t")[6]))
            info_dicts[line.split("\t")[0]].append(line.split("\t")[7])
            info_dicts[line.split("\t")[0]].append(line.split("\t")[8])
            info_dicts[line.split("\t")[0]].append(line.split("\t")[11])
            info_dicts[line.split("\t")[0]].append(line.split("\t")[19])

    with open(current_path + "/" + args.output, "w+") as info_writer:
        col_header = ["assembly_accession", "refseq_category", "taxid", "speciestaxid", "organism_name", "infraspecific_name", "assembly_level", "ftp_path"]
        csv_writer = csv.DictWriter(info_writer, fieldnames=col_header)
        csv_writer.writeheader()
        for k,v in info_dicts.items():

            csv_writer.writerow({"assembly_accession":k, "refseq_category":v[0],
                                  "taxid":v[1], "speciestaxid":v[2],
                                  "organism_name":v[3], "infraspecific_name":v[4],
                                  "assembly_level":v[5], "ftp_path":v[6]})
    cmd1 = "rm ./.tmp"
    subprocess.check_output(cmd1,shell=True)


if __name__ == "__main__":

    current_path = os.getcwd()

    parser = argparse.ArgumentParser("exclude information from genbank_assembly_summary")
    parser.add_argument("-p", "--path",type=str, help="genbank_assembly_summary.txt file_path")
    parser.add_argument("-f", "--file", type=str, help="genbank_assembly_summary.txt file_name")
    parser.add_argument("-o","--output",type=str, help="output file")
    args = parser.parse_args()
    exclude_gb_info(current_path)
