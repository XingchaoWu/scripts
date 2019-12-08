#_*_coding:UTF-8_*_

import argparse
import subprocess
# import pandas as pd
"""
1.根据taxid匹配url
2.下载参考序列
3.建立bowtie2索引
"""

# 获得参考基因组下载地址（url）

def obtain_ref_url():
    # 通过taxid读取csv文件中数据，获取物种信息
    # 0 assembly_accession
    # 1 refseq_category  "reference genome"、"representative genome"、"na"
    # 2 taxid
    # 3 speciestaxid
    # 4 organism_name
    # 5 infraspecific_name
    # 6 assembly_level   "Complete genome"、"Chromosome"、"Scaffold"、"Contig"
    # 7 ftp_path

    # csv文件中提取url
    # df = pd.read_csv(args.path + "/" + args.search_file)
    # df = df.values
    # for row_info in df:
    #     if args.taxid == row_info[2]: # 判断输入的taxid是否和taxid一致
    #         print("refseq_category " + "\t" + row_info[2])
    #         print("assembly level" + "\t" + row_info[6])
    #         # 判断
    #         if row_info[1] == "na":
    #             break
    #         else:
    #             pass

    # 根据taxid从下载的assembly_summary_genbank.txt文件中提取url
    line_num = 0
    with open(args.path + "/" + args.search_file,"r",encoding="utf-8") as in_file:
        for line in in_file:
            if line_num > 2:
                line_split = line.strip().split("\t")
                if args.taxid == line_split[6]:  # 输入种的taxid进行索引匹配数据
                    if line_split[4] == "reference genome" or line_split[4] == "representative genome" :
                        url = line_split[19]
                        print(url)
                    else:
                        pass

                else:
                    continue

            else:
                line_num += 1












# 下载参考基因组并解压构建索引

def download_ref():
    bowtie2_build_path = ""
    # ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/803/615/GCA_001803615.1_ASM180361v1/GCA_001803615.1_ASM180361v1_genomic.fna.gz
    url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/803/615/GCA_001803615.1_ASM180361v1"
    cmd0 = "wget -O " + args.genomefile_path + " " + url + "/" + url.split("/")[-1] + "_genomic.fna.gz"
    cmd1 = "gunzip " + url.split("/")[-1] + "_genomic.fna.gz"
    cmd2 = bowtie2_build_path + " " + url.split("/")[-1] + "_genomic.fna" + " " + url.split("/")[-1] + "_genomic"
    subprocess.check_output(cmd0,shell=True)
    subprocess.check_output(cmd1,shell=True)
    subprocess.check_output(cmd2,shell=True)


# 将unmapped数据与参考基因组进行比对
def align():
    pass



if __name__ == "__main__":
    # pass
    parser = argparse.ArgumentParser("Reference sequence download and sample data align with special species's genome ")
    parser.add_argument("-t", "--taxid", type=str, help="taxid")
    parser.add_argument("-s", "--search_file",type=str, help="search file,like *.csv")
    parser.add_argument("-p", "--path",type=str,help="the path of search file. for example /home/data")
    args = parser.parse_args()