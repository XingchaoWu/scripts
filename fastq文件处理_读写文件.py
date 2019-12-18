#_*_coding:UTF-8_*_

import gzip
import sys
# 定义函数读取fastq文件
def read_fastq(seq, input_file_path):
    with gzip.open(input_file_path,'rb') as input_file:
        NR = 0 # NR 读取数据的行数数值，初始值为0
        for line in input_file:
            if NR %4 == 0:
                seq_id = line.decode()  # 对二进制文件解码
                seq[seq_id] = ""
            else:
                seq[seq_id] += line.decode()
            NR += 1
    input_file.close()


# 定义函数写入fastq
def write_fastq(seq, output_file_path):
    with gzip.open(output_file_path,'wb') as output_file:
        for key, value in seq.items():  # 遍历上一步得到的字典，并将其写入到新的文件中
            # print(key,value)
            output_file.write(key.encode())  # 将str转换为二进制文件
            output_file.write(value.encode())

    output_file.close()


if __name__ == "__main__":
    seq = {}  # 建立空字典键存储序列id信息，值存储剩下三行信息（包括“序列”、“+”、“质量值”）
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    read_fastq(seq,input_file_path)
    write_fastq(seq,output_file_path)