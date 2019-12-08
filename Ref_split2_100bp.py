#_*_coding:UTF-8_*_
# import math
import argparse
# 读取参考基因组序列，并建立字典存储
def read_fasta():
    # fa_split_100bp = {}
    with open(r"D:\My Projects\02_参考基因组处理\GCA_003069565.1_ASM306956v1_genomic.fna","r") as source_file:
        for line in source_file:
            if line.startswith(">"):
                fa_split_id =line.rstrip("\n")
                fa_split_100bp[fa_split_id] =""
            else:
                fa_split_100bp[fa_split_id] += line.rstrip("\n")
        # print(fa_split_100bp)
    source_file.close()

# 对参考序列进行切分成100bp的片段
def split_fasta2_100bp():
    with open(r"D:\My Projects\02_参考基因组处理\GCA_003069565.1_ASM306956v1_100_genomic.fna","w") as target_file:
        for id in fa_split_100bp.keys():
            # print(len(fa_split_100bp[id]))
            i = 1
            # for n in range(math.ceil(len(fa_split_100bp[id])/50)):
            for n in range(int(len(fa_split_100bp[id])/50)):
                target_file.write(id + (("|split_{}").format(i)) + "\n")
                target_file.write(fa_split_100bp[id][n*50:100+n*50] + "\n")
                i += 1

    target_file.close()

# 读取比对后未比对上的序列




if __name__ == "__main__":
    fa_split_100bp = {}
    # read_fasta()
    # split_fasta2_100bp()
    # parser = argparse.ArgumentParser(description=)
    # parser.add_argument("-i", "--inputfile", type=str, help="input file for being splited")
    # parser.add_argument("-o", "--outputfile", type=str, help="output file")
    # args = parser.parse_args()
    read_fasta()
    split_fasta2_100bp()


