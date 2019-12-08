#_*_coding:UTF-8_*_
import argparse
import os

def accession(accession_taid_dict):
    with open(args.accession_path,"r") as in_acc:
        for line in in_acc:
            line = line.strip().split("\t")
            accession_taid_dict[line[1]] = line[2]
    return accession_taid_dict

def accession2taxid(accession_taid_dict,fasta_dict,cur_path):
    line_num = 0
    with open(args.input_file,"r") as in_fasta:
        with open(cur_path + "/" + args.output_file, "w+") as out_fasta:
            for line in in_fasta:
                line = line.strip("\n")
                if line_num % 2 == 0:
                    seq_k = line.split(" ")[0][1:]
                    fasta_dict[seq_k] = ""
                else:
                    seq_v = line
                    fasta_dict[seq_k] += seq_v
                line_num += 1

            for k_seq in fasta_dict.keys():
                print(k_seq)
                for k_ac in accession_taid_dict.keys():
                    if k_seq == k_ac:
                        out_fasta.write(">" + k_ac + " |" + " kraken:taxid |  " + accession_taid_dict[k_ac] + "  " + k_ac + "  |" + "\n")
                        out_fasta.write(fasta_dict[k_seq] + "\n")
                    else:
                        continue
    in_fasta.close()
    out_fasta.close()
def main():
    cur_path = os.getcwd()
    accession_taid_dict = {}
    fasta_dict = {}
    accession(accession_taid_dict)
    accession2taxid(accession_taid_dict,fasta_dict,cur_path)

if __name__ =="__main__":
    parser = argparse.ArgumentParser("Format fasta file sequence")
    parser.add_argument("-ac", "--accession_path", type=str, help="accession2taxid files path, 'absolute_path'")
    parser.add_argument("-in", "--input_file", type=str, help="input fasta file need to be format,'absolute_path'")
    parser.add_argument("-o","--output_file", type=str, help="output fasta file")
    args = parser.parse_args()
    main()