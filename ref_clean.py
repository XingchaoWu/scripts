#_*_coding:UTF-8_*_
import argparse
from collections import defaultdict


# 读取原始数据并生成去除污染序列短序列
def remove_seq():
    origin_splited_dict = {}
    # gene_id = []
    # 读取原始序列文件
    # with open(args.input_ref_file,"r") as origin_file:
    with open(r"D:\My Projects\02_参考基因组处理\GCA_003069565.1_ASM306956v1_100_genomic.fna","r") as origin_file:
        for line in origin_file:
            if line.startswith(">"):
                id = line.rstrip("\n")
                # gene_id.append(id.split("|")[0])
                origin_splited_dict[id] = ""
            else:
                origin_splited_dict[id] = line.rstrip("\n")
    # print(len(origin_splited_dict))
    origin_file.close()


    # 读取比对上其他参考基因组的序列
    mapped_file_list = []

    # with open(args.input_mapped_file,"r") as mapped_file:
    with open(r"D:\My Projects\02_参考基因组处理\GCA_003069565.1_ASM306956v1.al.fasta","r") as mapped_file:
        for line in mapped_file:

            if line.startswith(">"):
                continue
            else:
                mapped_file_list.append(line.rstrip("\n"))
    # print(len(mapped_file_list))
    # print(gene_id)
    # print(mapped_file_list)
    mapped_file.close()


    # 生成新的去除比对上其他参考基因组的序列
    # with open(args.output_temp_file,"w") as new_file:
    with open(r"D:\My Projects\02_参考基因组处理\test.fasta","w") as new_file:
        for mapped_v in mapped_file_list:
            # print(mapped_v)
            for origin_splited_dict_k, origin_splited_v in list(origin_splited_dict.items()):   # 字典在遍历时，不能进行修改，若需要修改，可先将其转化为列表
                if mapped_v == origin_splited_v.upper():
                    # del origin_splited_dict[origin_splited_dict_k]  # 删除
                    origin_splited_dict[origin_splited_dict_k] = "N" * 100  # 比对上的序列用N代替

        for k in origin_splited_dict.keys():
            new_file.write(k + "\n")
            new_file.write(origin_splited_dict[k] + "\n")

    new_file.close()

def assembly_seq():
    """
    序列拼接
    :return: None
    """
    # join 拼接
    # 读取去除污染序列文件，并转换为一键映射多个值的字典
    assembly_dict = {}
    # with open(args.output_temp_file,"r") as file1:
    with open(r"D:\My Projects\02_参考基因组处理\test.fasta","r") as file1:
        for line in file1:
            if line.startswith(">"):
                id1 = line.rstrip("\n")
                assembly_dict[id1] = ""
            else:
                assembly_dict[id1] = line.rstrip("\n")
        # print(assembly_dict)
    assembly_dict_list =list(assembly_dict.items())
    # print(assembly_dict_list)
    assembly_dict_new =defaultdict(list)
    for k, v in assembly_dict_list:
        id2 = k.split("|")[0]
        assembly_dict_new[id2].append(v)
    # print(assembly_dict_new)

    # 遍历字典并进行序列拼接
    # with open(args.output_join_file,"w") as file2:
    with open(r"D:\My Projects\02_参考基因组处理\GCA_003069565.1_ASM306956v1.clean.merge.fasta","w") as file2:
        for k1 , v1 in assembly_dict_new.items():
            #
            file2.write(k1 + "\n")
            file2.write(v1[0][:50])
            file2.write(v1[0][50:100])
            for n in range(1, len(v1)):
                seq = v1[n][50:100]
                file2.write(seq)
            file2.write("\n")



if __name__ == "__main__":
    fa_split_100bp = {}
    assembly_name = []
    # parse = argparse.ArgumentParser("Remove contaminated sequence from reference sequence")
    # parse.add_argument("-i", "--input_ref_file",type=str, help="Input original split reference genome sequence")
    # parse.add_argument("-I", "--input_mapped_file",type=str, help="Input alignment of reference genome sequences")
    # parse.add_argument("-o", "--output_temp_file",type=str, help="Output alignment of reference genome sequences")
    # parse.add_argument("-O", "--output_join_file",type=str, help="Output alignment of reference genome sequences")
    # args = parse.parse_args()
    remove_seq()
    assembly_seq()