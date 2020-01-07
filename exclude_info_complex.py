#_*_coding:UTF-8_*_
import os
import argparse
import subprocess
import re
import csv

# exclude sample_num
def exclude_sample_name(cur_path,sample_list):
    with open("%s/%s"%(cur_path,args.sample),"r") as list:
        for line in list:
            sample_name = line.strip().split("\t")[1]
            if re.findall("^[AR]",sample_name):
                sample_list.append(sample_name)
            else:
                continue
    list.close()

# generate dict of sample_name:complex
def exclude_info(cur_path,sample_list,complex_dict,complex_list):

    for sample in sample_list:
        complex_dict[sample] = []
        with open("%s/se_v1/%s/bracken/%s.kraken.report.txt"%(cur_path,sample,sample), "r") as report_txt:
            for line_info in report_txt:
                info = line_info.strip().split("\t")
                for id in complex_list:
                    if int(info[4]) == id:
                        complex_dict[sample].append({id:info[2]})
        report_txt.close()
    return complex_dict


# exclude sequences
def exclude_seq(cur_path,complex_dict):
    for k_sample,v_sample in complex_dict.items():
        mid_dict = {k: v for info in v_sample for k, v in info.items()}
        for k_id in mid_dict.keys():
            if int(mid_dict[k_id]) > 0 and int(mid_dict[k_id]) <= 10:
                grep_seq_id = "grep 'taxid %s' %s/se_v1/%s/bracken/%s.kraken.output.txt " \
                              "|awk -F '\t' '{print$2}' |sort|uniq > %s/se_v1/Infos_TMP/exclude_complex/tmp"\
                              %(k_id,cur_path,k_sample,k_sample,cur_path)

                exclude_seq = "cat %s/se_v1/Infos_TMP/exclude_complex/tmp |while read id ; " \
                                    "do grep -A 1 $id %s/se_v1/%s/bracken/%s.fastq.gz | " \
                                    "sed 's/@/>/g' >> %s/se_v1/Infos_TMP/exclude_complex/%s.%s.fasta; done"\
                                    %(cur_path,cur_path,k_sample,k_sample,cur_path,k_sample,k_id)
                subprocess.check_output(grep_seq_id,shell=True)
                subprocess.check_output(exclude_seq,shell=True)

                rm_file = "rm %s/se_v1/Infos_TMP/exclude_complex/tmp"%(cur_path)
                subprocess.check_output(rm_file,shell=True)
    tar_cmd = "cd  %s/se_v1/Infos_TMP/exclude_complex/ && tar -zcvf %s.tar.gz *"%(cur_path,args.batch)
    subprocess.check_output(tar_cmd,shell=True)

# write info into csv file
def write_info(cur_path,complex_dict):
    with open("%s/se_v1/Infos_TMP/exclude_complex/%s_all_complex.csv" %(cur_path,args.batch),"w") as out_csv:
        header = ["Sample_Name", "M_tuberculosis_c(77643)",
                  "M_avium_c(120793)", "E_cloacae_c(354276)",
                  "A_baumannii_c(909768)"]
        write_file = csv.DictWriter(out_csv, fieldnames=header)
        write_file.writeheader()
        for k,value in complex_dict.items():
            mid_dict = {k:v for info in value for k,v in info.items()}
            write_file.writerow({"Sample_Name":k,
                                 "M_tuberculosis_c(77643)":mid_dict[77643],
                                 "M_avium_c(120793)":mid_dict[120793],
                                 "E_cloacae_c(354276)":mid_dict[354276],
                                 "A_baumannii_c(909768)":mid_dict[909768]})
    out_csv.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("exclude the number of complex")
    parser.add_argument("-b","--batch",type=str,help="the analysis batch")
    parser.add_argument("-s","--sample",type=str, help="the file name of sample.list")
    args = parser.parse_args()
    cur_path = os.getcwd()
    complex_list = [77643,120793,354276,909768]
    sample_list = []
    complex_dict = {}
    exclude_sample_name(cur_path,sample_list)
    # judge the filedir is existed
    file = os.path.exists("%s/se_v1/Infos_TMP/exclude_complex"%(cur_path))
    if file == True:
        exclude_info(cur_path, sample_list,complex_dict,complex_list)
        write_info(cur_path,complex_dict)
        exclude_seq(cur_path, complex_dict)
    else:
        mkdir_cmd = "mkdir %s/se_v1/Infos_TMP/exclude_complex"%(cur_path)
        subprocess.check_output(mkdir_cmd,shell=True)
        exclude_info(cur_path, sample_list,complex_dict,complex_list)
        write_info(cur_path, complex_dict)
        exclude_seq(cur_path, complex_dict)