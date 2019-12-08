#_*_coding:UTF-8_*_

import os
import argparse
import subprocess
import xlrd, xlwt
import re

def obtain_genenum2vfnum(cur_path):

    VFs_name_num_dicts = {}
    cmd = "grep '>' VFDB_setA_nt.fa > .tmp"
    subprocess.check_output(cmd, shell=True)
    with open("./.tmp","r") as tmp:
        for line_info in tmp:
            line_info = line_info.strip()
            special_list = [">VFG000476(gb|AAG03023) (grvA) gifsy-2 related virulence gene [GrvA (VF0110)] [Salmonella enterica (serovar typhimurium)]",
                            ">VFG001799(gb|CAB94853) (map) extracellular proteins Map [Eap/Map (VF0016)] [Staphylococcus aureus str. Newman D2C (ATCC 25904)]"]
            if line_info in special_list:
                line_info = line_info[:-2]
                pattern1 = re.compile(r'[[](.*?)[)]]', re.S)  # 匹配含VFs_name信息
                pattern2 = re.compile(r'[(](.*?)[)]', re.S)  # 匹配含VFs_num信息
                line_info_1 = re.findall(pattern1, line_info)
                line_info_2 = re.findall(pattern2, line_info)
                line_char = line_info_1[0].split(" ")[:-1]  # 提取VFs_name信息
                VF_name = " ".join(line_char)
                VF_num = line_info_2[-1]  # 提取VFs_num信息
                VFs_name_num_dicts[VF_name] = VF_num
                print(VF_name + "\t" + VF_num)
            else:
                pattern1 = re.compile(r'[[](.*?)[)]]', re.S)  # 匹配含VFs_name信息
                pattern2 = re.compile(r'[(](.*?)[)]', re.S)  # 匹配含VFs_num信息
                line_info_1 = re.findall(pattern1, line_info)
                line_info_2 = re.findall(pattern2, line_info)
                line_char = line_info_1[0].split(" ")[:-1]  # 提取VFs_name信息
                VF_name = " ".join(line_char)
                VF_num = line_info_2[-1]  # 提取VFs_num信息
                VFs_name_num_dicts[VF_name] = VF_num

    in_xls = xlrd.open_workbook(cur_path + "/" + args.xls,"r")
    in_xls_table = in_xls.sheet_by_index(0)
    out_xls = xlwt.Workbook()
    out_xls_table = out_xls.add_sheet("vfs_full", cell_overwrite_ok=True)
    rows = in_xls_table.nrows
    cols = in_xls_table.ncols
    for i in range(1,rows):
        for j in range(cols):
            value = in_xls_table.cell(i,j).value
            out_xls_table.write(i-1,j, value)

    for i in range(1, rows):
        value_0 = in_xls_table.cell(i,0).value
        # print(value_0)
        for k in VFs_name_num_dicts.keys():
            # print(VFs_name_num_dicts[k])
            if value_0 == VFs_name_num_dicts[k]:
                # print("True")
                out_xls_table.write(0, cols, "VF_ID")
                out_xls_table.write(i, cols, VFs_name_num_dicts[k])

    out_xls.save(r"D:\My Projects\04_vfdb格式化\VFs_out.xls")


def VF_gene_map_VF_num(cur_path):
    cmd = "grep '>' VFDB_setA_nt.fa > .tmp"
    subprocess.check_output(cmd, shell=True)
    with open(cur_path + "/" + ".tmp","r") as in_txt:
        with open(r"D:\My Projects\04_vfdb格式化\tmp.txt","w") as out_txt:

            for line in in_txt:
                line = line.strip()[1:]
                # print(line)
                VF_gene_num = line.split(" ")[0]
                line = line.strip()
                pattern = re.compile(r'[(](.*?)[)]', re.S)
                VF_num = re.findall(pattern, line)[-1]
                if len(VF_num) != 0: # 判断是否为null
                    out_txt.write(VF_gene_num + "\t" + VF_num + "\n")
                else:
                    out_txt.write(VF_gene_num + "\t" + "-" + "\n")
    in_txt.close()
    out_txt.close()
    rm_tmp = "rm ./.tmp"
    subprocess.check_output(rm_tmp, shell=True)


def formate_vfdb(cur_path):
    with open(cur_path + "/" + args.fasta ,"r") as in_fasta:
        with open(cur_path + "/" + args.fasta.split(".")[:-1] + "_formate.fasta" ,"w") as out_fasta:
            for line in in_fasta:
                line = line.strip()[1:]
                pattern = re.compile(r'[(](.*?)[)]', re.S)
                num = re.findall(pattern, line)[-1]
                if line.startswith(">"):
                    gene_num = line.strip()[1:].split(" ")[0]
                    out_fasta.write(gene_num + " | " + num + "\n")
                else:
                    out_fasta.write(line)
    in_fasta.close()
    out_fasta.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Format the sequence file, retaining only the virulence gene number "
                                     "and obtaining the virulence_gene_number to virulence_factor_number mapping")
    parser.add_argument("-f", "--fasta", type=str, help="VFDB fasta file")
    parser.add_argument("-x", "--xls", type=str, help="VFs description file")
    parser.add_argument("-o", "--outfile", type=str, help="output file")
    parser.add_argument("-v", "--vfdb", type=str, help="only run formate_vfdb.py")
    args = parser.parse_args()
    parser.add_argument()
    cur_path = os.getcwd()
    if args.vfdb == "":
        formate_vfdb(cur_path)
    else:
        obtain_genenum2vfnum(cur_path)
