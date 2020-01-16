#_*_coding:UTF-8_*_

import os
import argparse
import subprocess
import re
import csv
import threading

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
            if int(mid_dict[k_id]) > 0 and int(mid_dict[k_id]) <= 50:
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


# write info into csv file
def write_info(cur_path,complex_dict):
    with open("%s/se_v1/Infos_TMP/exclude_complex/%s_all_complex.csv"%(cur_path,args.batch),"w") as out_csv:
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

# 修改于20200114 增加曲霉属序列提取
# exclude the sequences of Aspergillus genus(taxid 5052)
def exclude_aspergillus_seq(cur_path,sample_list):
    for sample in sample_list:
        grep_seq_id = "grep 'taxid 5052' %s/se_v1/%s/bracken/%s.kraken.output.txt " \
                      "|awk -F '\t' '{print$2}' |sort|uniq > %s/se_v1/Infos_TMP/exclude_complex/tmp1"\
                      %(cur_path,sample,sample,cur_path)
        exclude_seq = "cat %s/se_v1/Infos_TMP/exclude_complex/tmp1 |while read id ; " \
                            "do grep -A 1 $id %s/se_v1/%s/bracken/%s.fastq.gz | " \
                            "sed 's/@/>/g' >> %s/se_v1/Infos_TMP/exclude_complex/%s.5052.fasta; done"\
                            %(cur_path,cur_path,sample,sample,cur_path,sample)
        subprocess.check_output(grep_seq_id,shell=True)
        subprocess.check_output(exclude_seq,shell=True)
        rm_file = "rm %s/se_v1/Infos_TMP/exclude_complex/tmp1"%(cur_path)
        subprocess.check_output(rm_file,shell=True)

# exclude the info of Human mastadenovirus B 修改与20200115 人腺病毒分型
def exclude_Human_mastadenovirus_B_info(cur_path,sample_list):
    Human_mastadenovirus_B_list = [108098,565302,10519,565303,198503,10522]
    Human_mastadenovirus_B_dict = {}
    for sample in sample_list:
        Human_mastadenovirus_B_dict[sample] = []
        with open("%s/se_v1/%s/bracken/%s.kraken.report.txt"%(cur_path,sample,sample), "r") as report_txt:
            for line_info in report_txt:
                info = line_info.strip().split("\t")
                for i in Human_mastadenovirus_B_list:
                    if int(info[4]) == i:
                        Human_mastadenovirus_B_dict[sample].append({i:info[2]})
        report_txt.close()
    # write to csv
    with open("%s/se_v1/Infos_TMP/exclude_complex/%s_Human_mastadenovirus_B_info.csv" % (cur_path, args.batch), "w") as Human_mastadenovirus_B_csv:
        header = ["Sample_Name", "hmb(108098)",
                  "hab1(565302)", "ha7(10519)",
                  "hab2(565303)","sa21(198503)","ha35(10522)"]
        write_file = csv.DictWriter(Human_mastadenovirus_B_csv, fieldnames=header)
        write_file.writeheader()
        for k, value in Human_mastadenovirus_B_dict.items():
            m_dict = {k: v for info in value for k, v in info.items()}
            write_file.writerow({"Sample_Name": k,
                                 "hmb(108098)": m_dict[108098],
                                 "hab1(565302)": m_dict[565302],
                                 "ha7(10519)": m_dict[10519],
                                 "hab2(565303)": m_dict[565303],
                                 "sa21(198503)": m_dict[198503],
                                 "ha35(10522)": m_dict[10522]})
    Human_mastadenovirus_B_csv.close()

# main
def main(cur_path, sample_list, complex_dict, complex_list):
    exclude_info(cur_path, sample_list, complex_dict, complex_list)
    write_info(cur_path, complex_dict)
    exclude_seq(cur_path, complex_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("exclude the number of complex",
                                     usage="\npython exclude_complex_info.py -s [sample.list] -b [batch]")
    parser.add_argument("-b","--batch",type=str,help="the analysis batch")
    parser.add_argument("-s","--sample",type=str, help="the file name of sample.list")
    args = parser.parse_args()
    cur_path = os.getcwd()
    complex_list = [77643,120793,354276,909768]
    sample_list = []
    complex_dict = {}
    exclude_sample_name(cur_path,sample_list)

    # judge the file_dir is existed
    file = os.path.exists("%s/se_v1/Infos_TMP/exclude_complex"%(cur_path))
    if file == True:
        rm_file = "rm %s/se_v1/Infos_TMP/exclude_complex/*"%(cur_path)
        os.system(rm_file)
        thread_exclude_aspergillus_seq = threading.Thread(target=exclude_aspergillus_seq,args=(cur_path, sample_list))
        thread_main = threading.Thread(target=main,args=(cur_path, sample_list, complex_dict, complex_list))
        thread_exclude_Human_mastadenovirus_B_info = threading.Thread(target=exclude_Human_mastadenovirus_B_info,args=(cur_path,sample_list))
        thread_exclude_aspergillus_seq.start()
        thread_main.start()
        thread_exclude_Human_mastadenovirus_B_info.start()
        thread_exclude_aspergillus_seq.join()
        thread_exclude_Human_mastadenovirus_B_info.join()
        thread_main.join()
        tar_cmd = "cd  %s/se_v1/Infos_TMP/exclude_complex/ && tar -zcvf %s_complex.tar.gz *" %(
        cur_path, args.batch)
        subprocess.check_output(tar_cmd, shell=True)
    else:
        mkdir_cmd = "mkdir %s/se_v1/Infos_TMP/exclude_complex"%(cur_path)
        subprocess.check_output(mkdir_cmd,shell=True)
        thread_exclude_aspergillus_seq = threading.Thread(target=exclude_aspergillus_seq,args=(cur_path, sample_list))
        thread_main = threading.Thread(target=main,args=(cur_path, sample_list, complex_dict, complex_list))
        thread_exclude_Human_mastadenovirus_B_info = threading.Thread(target=exclude_Human_mastadenovirus_B_info,args=(cur_path, sample_list))
        thread_exclude_aspergillus_seq.start()
        thread_main.start()
        thread_exclude_Human_mastadenovirus_B_info.start()
        thread_exclude_aspergillus_seq.join()
        thread_main.join()
        thread_exclude_Human_mastadenovirus_B_info.join()
        tar_cmd = "cd  %s/se_v1/Infos_TMP/exclude_complex/ && tar -zcvf %s_complex.tar.gz *" %(
        cur_path, args.batch)
        subprocess.check_output(tar_cmd, shell=True)
