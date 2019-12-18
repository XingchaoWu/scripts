#_*_coding:UTF-8_*_

NR = 0
seq_id = []
with open(r"D:\My Projects\fastq文件处理\A190912PEPN015.my_tb.mapped.fasta", "r") as file1:
    for line in file1:
        if NR % 2 == 0:
            # print(line)
            seq_id.append(line.strip("\n").split(" ")[0].replace(">",""))
        NR += 1
print(len(seq_id))
file1.close()

kraken = {}
with open(r"D:\My Projects\fastq文件处理\A190912PEPN015.kraken.output.txt", "r") as file2:
    for line in file2:
        # print(line)
        kraken_id = line.split("\t")[1]
        # print(kraken_id)
        kraken[kraken_id] = line.split("\t")[2:3]
        # print(line.split("\t")[2:3])
file2.close()
with open(r"D:\My Projects\fastq文件处理\A190912PEPN015.match.txt", "w") as file3:
    for id in seq_id:
        # print(i)
        for k in kraken.keys():
            if id == k:
                # print(id)
                taxon_info = "".join(kraken[id])  # 列表转化为字符串
                file3.write(id + " " + taxon_info + "\n")
