#_*_coding:UTF-8_*_
import gzip

"""
运行速度慢
增加线程运行
统计存放id信息文件包含id信息的条数，将其分割成多个temp文件
调用多线程执行对每个文件分别读取、写入，最后将这些文件合并成一个文件。

"""
###  待修改


def read_fastq(exclude_read):
    """
    根据reads id提取read（从fastq文件或者fasta文件中提取reads）
    读取id信息
    读取原始fastq序列信息如果序列编号信息匹配提取该序列以及接下来的一行写入fa文件中
    :param exclude_read:
    :return:
    """
    NR = 0  # 起始行为0
    with gzip.open(r"D:\My Projects\fastq文件处理\A190827BCPN002.non_human.exclude.fastq.gz","rb") as fastq_file:  # 打开fastq文件
        for line in fastq_file:  # 遍历该文件并按照字典的格式写入新建的空白字典中
            if NR % 2 == 0 :
                # id = line.decode()
                # id = line.lstrip(">").rstrip(" 1:N:0").decode()
                id = line.startswith(">")
                exclude_read[id] = ""
            else:
                exclude_read[id] += line.decode()
            NR += 1
    fastq_file.close()
def read_id(ids):
    with open(r"D:\My Projects\fastq文件处理\002.txt", "r") as id_file:
        for line in id_file:
            ids.append(">" + line.strip("\n") + " 1:N:0")
    id_file.close()


def match(ids,exclude_read):
    with open(r"D:\My Projects\fastq文件处理\A190827BCPN002.5052clean.fasta","w") as outfile:  # 新建一个文件用于写入文件
        for id in ids:  # 遍历存储序列编号的文件
            for k in exclude_read.keys():
                if id == k.strip("\n"):
                    outfile.write(k.replace("@",">"))
                    outfile.write(exclude_read[k].split("\n")[0] + "\n")  # 按照"\n"切割数据，index[0]为序列信息

                else:
                    continue

    outfile.close()


if __name__ == "__main__":
    exclude_read = {}  # 新建空字典用于暂时存储读取的数据
    ids = []
    read_fastq(exclude_read)
    read_id(ids)
    match(ids,exclude_read)