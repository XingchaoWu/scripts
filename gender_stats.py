#_*_coding:UTF-8_*_

import os
import argparse
import re
import csv
import subprocess

def obtain_sample(cur_path,sample_list):
    # 读取样本信息，去除NTC和其他非商业样本
    with open(cur_path + "/" + args.sample_list,"r") as in_list:
        for info in in_list:
            info = info.strip().split("\t")
            if re.findall("^[AR]",info[1]):
                sample_list.append(info[1])
            else:
                continue
    return sample_list

# 统计 'x' 'y' 序列数并判断性别
def gender_stats(cur_path,sample_list):
    sex_dict = {}
    for sample in sample_list:
        count_cmd = "grep -v '@' " + cur_path + "/se_v1/" + sample + "/map/" \
                    + sample +".sam  |awk -F '\t' '{print$3}' |sort|uniq -c > " \
                    + cur_path + "/se_v1/Infos_TMP/sex_stats/"+ sample + ".txt"
        os.system(count_cmd)
        sex_dict[sample] = []
        X_cmd = "grep 'X' " + cur_path + '/se_v1/Infos_TMP/sex_stats/'+ sample + ".txt" + "|awk -F ' ' '{print$1}' >> .tmp"
        Y_cmd = "grep 'Y' " + cur_path + '/se_v1/Infos_TMP/sex_stats/'+ sample + ".txt" + "|awk -F ' ' '{print$1}' >> .tmp"
        subprocess.check_output(X_cmd,shell=True)
        subprocess.check_output(Y_cmd,shell=True)
        with open(cur_path + "/.tmp","r") as in_tmp:
            for num in in_tmp:
                sex_dict[sample].append(int(num.rstrip("\n")))
        rm_tmp = "rm " + cur_path + "/.tmp"
        subprocess.check_output(rm_tmp,shell=True)
    print(sex_dict)

    with open(cur_path + "/se_v1/Infos_TMP/sex_stats/PM19453_sex_stats.csv", "w") as write_file:
        col_header = ["sample_num", "X", "Y", "Ratio", "sex"]
        csv_writer = csv.DictWriter(write_file, fieldnames=col_header)
        csv_writer.writeheader()
        for k,v in sex_dict.items():
            if v[0] / v[1] >= 13:
                gender = "F"
            else:
                gender = "M"
            csv_writer.writerow({"sample_num": k, "X":v[0] , "Y": v[1], "Ratio": v[0] / v[1], "sex": gender})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="")
    parser.add_argument("-s", "--sample_list",type=str,help="sample.list")
    parser.add_argument("-b", "--batch",type=str, help="batch")
    args = parser.parse_args()
    cur_path = os.getcwd()
    sample_list = []
    obtain_sample(cur_path,sample_list)
    # 判断文件夹是否存在
    if os.path.exists(cur_path + "/se_v1/Infos_TMP/sex_stats") == True:
        gender_stats(cur_path,sample_list)
    else:
        mkdir = "mkdir " + cur_path + "/se_v1/Infos_TMP/sex_stats"
        gender_stats(cur_path,sample_list)