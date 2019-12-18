#_*_coding:UTF-8_*_
import gzip
import csv
# import sys
# import pandas as pd

def read_fastq(seq, input_file_path):  # 读取fastq文件
    with gzip.open(input_file_path,'rb') as input_file:
    #with gzip.open(input_file_path, 'rb') as input_file:
        NR = 0 # NR 读取数据的行数数值，初始值为0
        for line in input_file:
            if NR %4 == 0:
                seq_id = line.decode()  # 对二进制文件解码
                seq[seq_id] = ""
            else:
                seq[seq_id] += line.decode()
            NR += 1
    input_file.close()


def fq_to_fa():  # fastq转换为fasta
    # 保留序列id信息，并将开头的@替换为>，写入第二行的序列信息
    # read_fastq()
    with open(fa_output_file_path,'w') as fa_output_file:
        for key, value in seq.items():  # 遍历上一步得到的字典，并将其写入到新的文件中
            key = key.replace("@",">")  # 将序列编号的第一个字母"@"替换为">"
            # print(key[0],value.split("\n")[0])
            fa_output_file.write(key)
            fa_output_file.write(value.split("\n")[0] + "\n")  # 由于以"\n"作为分隔符拆分数据，所以需要在末尾加上"\n"进行换行
    fa_output_file.close()

"""
def GC_content():  # GC含量统计,并将统计结果写入csv文件
    data = []
    for key, value in seq.items():
        key = key.split("\n")[0]
        value = value.split("\n")[0]
        # A_count = value.count("A")  # 统计序列中碱基A的个数
        G_count = value.count("G")  # 统计序列中碱基G的个数
        C_count = value.count("C")  # 统计序列中碱基C的个数
        # T_count = value.count("T")  # 统计序列中碱基T的个数
        gc_content = (G_count + C_count) / len(value)*100
        # gc_content = (G_count + C_count) / (A_count + T_count + G_count + C_count)*100
        data.append((key,value,gc_content))
    with open(r"D:\My Projects\01_test\tem.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for list in data:
            csv_writer.writerow(list)
    csv_file.close()

"""
def read_exclude():  # 根据reads id 进行read 提取 （从fastq文件或者fasta文件中提取reads）
    pass


def write_fastq(seq, output_file_path):  # fastq文件写入
    with gzip.open(output_file_path,'wb') as output_file:
        for key, value in seq.items():  # 遍历上一步得到的字典，并将其写入到新的文件中
            # print(key,value)
            output_file.write(key.encode())  # 将str转换为二进制文件
            output_file.write(value.encode())
    output_file.close()


if __name__ == "__main__":
    seq = {}  # 建立空字典键存储序列id信息，值存储剩下三行信息（包括“序列”“+”“质量值”）
    # input_file_path = sys.argv[1]
    input_file_path = r"D:\My Projects\01_test\SRR8578913_1.fastq.gz"
    # output_file_path = sys.argv[2]
    output_file_path = r"D:\My Projects\01_test\test_2.fastq.gz"
    fa_output_file_path = r"D:\My Projects\01_test\test_2.fa"
    read_fastq(seq,input_file_path)
    # write_fastq(seq,output_file_path)
    # fq_to_fa()
    GC_content()