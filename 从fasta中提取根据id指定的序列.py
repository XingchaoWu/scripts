#_*_coding:UTF-8_*_
# from Bio import SeqIO

def normal_exclude_seq():
    # 读取指定的fasta文件,将文件按照序列名和序列对应到字典中的键值
    seq_dict = {}
    exclude_ids = input("输入需要提取序列的id： ")
    with open(r"D:\My Projects\fastq文件处理\Penicillium_digitatum.fasta","r") as inputfile:
        # 以“>”分割数据
        for line in inputfile:
            line_swith = line.startswith(">")
            if line_swith == True:
                seq_id =line.strip("\n")
                seq_dict[seq_id] = ""
            else:
                seq_dict[seq_id] += line.strip("\n")
    # 输入要提取的id信息

    with open(r"D:\My Projects\fastq文件处理\tmp.fasta","w") as outputfile:
        for exclude_id in list(exclude_ids):
        # 判断匹配提取序列
            for i in seq_dict.keys():
                if exclude_id == i:
                    outputfile.write(i + "\n")
                    outputfile.write(seq_dict[i] + "\n")
    inputfile.close()
    outputfile.close()

# def new_exclude_seq():
#     # 调用biopython中的包
#     record = SeqIO.read(r"D:\My Projects\fastq文件处理\Penicillium_digitatum.fasta","fasta")
#     seq = record.seq
#     print(seq)


if __name__ == "__main__":
    # new_exclude_seq()
    normal_exclude_seq()

