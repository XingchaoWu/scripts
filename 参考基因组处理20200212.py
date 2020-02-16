#_*_coding:UTF-8_*_

"""
分割基因组序列至76bp,含38bp的overlap序列，并生成fastq格式文件
"""

def split_genome():
    # 去除序列分行
    # with open('%s/%s'%(cur_path,args.input_file)) as in_file:
    input_path = r'D:\My Projects\02_参考基因组处理'
    input_file = input("Original reference genome files:")
    with open("%s\\%s"%(input_path,input_file),'r') as in_file:
        # with open("%s/.tmp"%(cur_path),"w") as tmp:
        with open("%s\\tmp"%(input_path),"w") as tmp:
            for line in in_file:
                if line.startswith(">"):
                    tmp.write(line)
                else:
                    tmp.write(line.strip())
    in_file.close()
    tmp.close()

    title = ""
    seq = ""
    # with open("%s/.tmp"%(cur_path),'r') as tmp1:
    with open("%s\\tmp"%(input_path),'r') as tmp1:
            for line01 in tmp1:
                if line01.startswith(">"):
                    title = line01.strip()
                else:
                    seq = line01.strip()
    tmp1.close()

    # 序列分割成含overlap的fastq格式文件
    # with open("%s/%s.fastq"%(cur_path,args.input_file.split("_")[:1]), 'w') as outfile:
    with open("%s\\%s_%s_%s.fastq"%(input_path,input_file.split("_")[0],input_file.split("_")[1],input_file.split("_")[2]), 'w') as outfile:
        outfile.write(title.replace(">","@") + "\t" + "0" + "\n")
        outfile.write(seq[0:76] + "\n")
        outfile.write("+"  + "\n")
        outfile.write("H" * len(seq[0:76]) + "\n")
        for i in range(1,len(seq)-75):
            outfile.write(title.replace(">","@") + "\t" + str(i)+ "\n")
            outfile.write(seq[i:(75+i)] + "\n")
            outfile.write( "+"  + "\n")
            outfile.write("H" * len(seq[i:(75+i)]) + "\n")
    outfile.close()


if __name__ ==  "__main__":
    split_genome()