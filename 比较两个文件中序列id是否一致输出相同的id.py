#_*_coding:UTF-8_*_
"""
判断两个fasta文件中序列id是否一致，并输出相同的seq_id
"""
NR = 0
file1_dict ={}
inputfile1 = input("输入流程分类提取的fasta文件： ")
with open(r"D:\My Projects\fastq文件处理\{}".format(inputfile1), "r") as file1:
    for line in file1:
        if NR % 2 == 0:
            seq_id = line.strip("\n").split(" ")[0]
            file1_dict[seq_id] = ""
            # print(seq_id)
        else:
            file1_dict[seq_id] = line.strip("\n")
            # print(line)
        NR += 1
# print(len(file1_dict))
file1.close()


file2_dict = {}
inputfile2 = input("输入bowtie mapped后fasta文件： ")
with open(r"D:\My Projects\fastq文件处理\{}".format(inputfile2), "r") as file2:
    for line in file2:
        if NR % 2 == 0:
            seq_id = line.strip("\n").split(" ")[0]
            file2_dict[seq_id] = ""
            # print(seq_id)
        else:
            file2_dict[seq_id] = line.strip("\n")
            # print(line)
        NR += 1
# print(file2_dict)
# print(len(file2_dict))
file2.close()
# inputfile3 = input("输入要保存一致序列文件名： ")
# inputfile4 = input("输入要保存不一致序列文件名： ")
with open(r"D:\My Projects\fastq文件处理\{}.co.fasta".format(inputfile2.split(".")[0]), "w")as outputfile_1:
    with open(r"D:\My Projects\fastq文件处理\{}.unco.fasta".format(inputfile2.split(".")[0]), "w")as outputfile_2:
        for k_1 in file1_dict.keys():
            if k_1 in file2_dict.keys():
                outputfile_1.write(k_1 + "\n")
                outputfile_1.write(file2_dict[k_1] + "\n")
            else:
                outputfile_2.write(k_1 + "\n")
                outputfile_2.write(file1_dict[k_1] + "\n")
outputfile_1.close()
outputfile_2.close()


file1_key = []
file2_key = []
for k_1 in file1_dict.keys():
    file1_key.append(k_1)
for k_2 in file2_dict.keys():
    file2_key.append(k_2)

for i in range(len(file2_key)):
    if file2_key[i]  in file1_key:
        print(file2_key[i])


print("检出序列条数：{}".format(len(file1_key)))
print("比对提取出的序列条数：{}".format(len(file2_key)))



