#_*_coding:UTF-8_*_

import os
import subprocess
import argparse

def count_dup(cur_path,sample_list):
    with open(cur_path + "/" + args.sample,"r") as in_txt:
        for line in in_txt:
            line = line.strip().split("\t")
            sample_list.append(line[1])

    with open(cur_path + "/" + "dup_count.txt","w") as out_txt:
        out_txt.write("sample_num" + "\t" + "dup_ratio" + "\n")
        for sample in sample_list:
            before_dup_cmd = "zcat /home/pmd/analysis/"+args.batch+"/se_v1/"+sample+"/map/"+sample+".non_human.exclude.fastq.gz |wc -l"
            after_dup_cmd = "zcat /home/pmd/analysis/"+args.batch+"/se_v1/"+sample+"/map/"+sample+".non_human.exclude.dedup.fastq.gz |wc -l"
            before_dup_reads = subprocess.check_output(before_dup_cmd,shell=True)
            after_dup_reads = subprocess.check_output(after_dup_cmd,shell=True)
            before_dup_num = float(before_dup_reads.strip("\n")) /4
            after_dup_num = float(after_dup_reads.strip("\n")) /4
            dup_ratio = ((before_dup_num - after_dup_num) / before_dup_num * 100)
            out_txt.write(sample + "\t" + str('%.2f'%dup_ratio) + "\n")
    in_txt.close()
    out_txt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("cout the duplication ratio")
    parser.add_argument("-s","--sample",type=str,help="sample.list")
    parser.add_argument("-b","--batch",type=str,help="PM19444")
    args = parser.parse_args()
    cur_path = os.getcwd()
    sample_list = []
    count_dup(cur_path,sample_list)