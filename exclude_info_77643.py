# —*—coding:utf-8_*_

import os
import argparse

def exclude_info_77643(cur_path,sample_list):
    with open(cur_path + "/" + args.sample,"r") as list:
        for line in list:
            sample_name = line.strip().split("\t")[1]
            if "NTC" not in sample_name:
                sample_list.append(sample_name)
            else:
                continue
    list.close()

    with open(cur_path + "/se_v1/Infos_TMP/" + args.batch + "_Mycobacterium_tuberculosis_complex.txt", "w") as out_txt:
        out_txt.write("sample_name" + "\t" + "reads_num" + "\n")

        for sample in sample_list:
            with open(cur_path + "/se_v1/" + sample + "/bracken/" + sample +".kraken.report.txt", "r") as report_txt:
                for line_info in report_txt:
                    info = line_info.strip().split("\t")
                    if int(info[4]) == 77643 :
                        out_txt.write(sample + "\t" + info[2] + "\n")
            report_txt.close()
    out_txt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("exclude the number of Mycobacterium tuberculosis complex")
    parser.add_argument("-b","--batch",type=str,help="the analysis batch")
    parser.add_argument("-s","--sample",type=str, help="the file name of sample.list")
    args = parser.parse_args()
    cur_path = os.getcwd()
    sample_list = []

    exclude_info_77643(cur_path,sample_list)