# _*_coding:UTF-8_*_


import os
import argparse


def mv_filename(cur_path):
    with open(cur_path +"/"+ args.inputfile) as in_file:
        with open(cur_path + "/" + args.inputfile + "_merge","w") as out_file:
            for line in in_file:
                line = line.strip().split("\t")
                out_file.write(line[0]+"\t"+line[1]+"\t"+"L001")

    in_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("change the file name")
    parser.add_argument("-i", "--inputfile", type=str, help="The original name corresponds to the modified name")
    args = parser.parse_args()
    cur_path = os.getcwd()
    mv_filename(cur_path)