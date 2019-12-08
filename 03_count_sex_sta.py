#_*_coding:UTF-8_*_

import os
import subprocess
import argparse
import csv
from pathlib2 import Path

# 读取sample.list文件并生成list只包含样本信息
def generate_samplename(current_path,sample_lists_remove_NTC):
    sample_lists = []
    cmd_0 = "cat " + current_path + "/" + args.sample + "|" + "cut -f 2 > .id_tmp"

    # 判断文件夹是否存在，如果存在,直接跳过新建文件夹，生成文件进行覆盖
    # 如果不存在新建文件夹，写入
    # os.path.exists()
    target_file = Path(current_path + "/" + "sex_stats")
    if target_file.exists():
        cmd_2 = ("cat .id_tmp | while read id ; do grep -v '@' " + current_path[:-7] + args.batch +
                 "/se_v1/$id/map/$id.sam |awk -F '\t' '{print$3}' |sort|uniq -c > "
                 + current_path[:-7] + args.batch + "/sex_stats/$id.txt; done")
        cmd_3 = "rm .id_tmp"

        subprocess.check_output(cmd_0, shell=True)
        subprocess.check_output(cmd_2, shell=True)
        # 将样本编号写入列表用于后续分别统计比对到X或Y的reads数
        with open(current_path + "/" + ".id_tmp") as file:
            for line in file:
                sample_lists.append(line.rstrip("\n"))

        subprocess.check_output(cmd_3,shell=True)

    else:
        cmd_1 = "mkdir sex_stats"
        subprocess.check_output(cmd_1, shell=True)
        cmd_2 =("cat .id_tmp | while read id ; do grep -v '@' " + current_path[:-7] + args.batch +"/se_v1/$id/map/$id.sam "
                "|awk -F '\t' '{print$3}' |sort|uniq -c > " + current_path[:-7] + args.batch + "/sex_stats/$id.txt; done")
        cmd_3 = "rm .id_tmp"

        subprocess.check_output(cmd_0,shell=True)
        subprocess.check_output(cmd_2,shell=True)

        # 将样本编号写入列表用于后续分别统计比对到X或Y的reads数
        with open(current_path + "/" + ".id_tmp") as file:
            for line in file:
                sample_lists.append(line.rstrip("\n"))
        subprocess.check_output(cmd_3,shell=True)

    # 删除NTC样本
    for n in sample_lists:
        if "NTC" not in n:
            sample_lists_remove_NTC.append(n)
        else:
            continue
    return sample_lists_remove_NTC


def exclude_XY_stats(sample_lists_remove_NTC,XY_dicts,current_path):
    for i in sample_lists_remove_NTC:
        cmd_0 = "grep 'X' " + current_path + '/' + 'sex_stats' + '/' + i + ".txt" + "|awk -F ' ' '{print$1}' >> tmp"
        cmd_1 = "grep 'Y' " + current_path + '/' + 'sex_stats' + '/' + i + ".txt" + "|awk -F ' ' '{print$1}' >> tmp"
        subprocess.check_output(cmd_0, shell=True)
        subprocess.check_output(cmd_1, shell=True)
        XY_dicts[i] = []
        with open(current_path + '/' + "tmp") as f:
            for j in f:
                XY_dicts[i].append(int(j.rstrip('\n')))
        cmd_2 = "rm " + current_path + '/' + "tmp"
        subprocess.check_output(cmd_2,shell=True)


    with open(current_path + "/" + "sex_stats" + "/" + args.batch + "_sex_stats.csv", "w+") as write_file:
        col_header = ["sample_num", "X", "Y", "Ratio", "sex"]
        # col_header = ["sample_num", "X", "Y", "Ratio"]
        csv_writer = csv.DictWriter(write_file, fieldnames=col_header)
        csv_writer.writeheader()
        for k, v in XY_dicts.items():
            # 判断性别是male or female  修改于20191120
            if v[0]/v[1] >=10:
                gender = "F"
            else:
                gender = "M"
            csv_writer.writerow({"sample_num":k,"X":v[0], "Y":v[1], "Ratio":v[0]/v[1],"sex":gender})
            # csv_writer.writerow({"sample_num":k,"X":v[0], "Y":v[1], "Ratio":v[0]/v[1]})

if __name__ == "__main__":
    # /homw/pmd/analysis/PM19394/
    current_path = os.getcwd()
    # batch = current_path.split("/")[4]
    sample_lists_remove_NTC = []
    XY_dicts = {}

    parser = argparse.ArgumentParser("current_path,batch")
    parser.add_argument("-s", "--sample", type=str, help="input sample.list file")
    parser.add_argument("-b", "--batch", type=str, help="sample batch as 'PM19396'")
    args = parser.parse_args()
    generate_samplename(current_path,sample_lists_remove_NTC)
    exclude_XY_stats(sample_lists_remove_NTC,XY_dicts,current_path)
