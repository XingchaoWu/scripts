#_*_coding:UTF-8_*_

import xlrd
import argparse
import os

def filter_info(cur_path,xls_taxid,bracken_dict):
    # filter raw txt
    xls_data = xlrd.open_workbook(cur_path + "/" + args.xls_file)
    xls_table = xls_data.sheet_by_index(0)
    nrow = xls_table.nrows
    for i in range(1, nrow):
        taxid = xls_table.cell(i,0).value
        xls_taxid.append(int(taxid))

    with open(args.path + "/" + args.txt_file,"r") as in_txt:
        for line in in_txt:
            line = line.strip().split("\t")
            bracken_dict[line[1]] = [line[0],line[2],line[3],line[4],line[5],line[6]]
    in_txt.close()

    # /home/pmd/analysis/PM19436/se_v1/R191217OTPN016/bracken/R191217OTPN016.bracken.species.txt
    with open(args.path +"/"+args.txt_file.split(".")[:-1] + ".filter.txt","w") as out_txt:
        out_txt.write("name" +"\t"+ "taxonomy_id" +"\t"+ "taxonomy_lvl" +"\t"
                      + "kraken_assigned_reads" +"\t"+ "added_reads" +"\t"
                      + "new_est_reads" +"\t"+ "fraction_total_reads" + "\n")
        for id in xls_taxid:
            for bracken_k in bracken_dict.keys():
                if str(id) == bracken_k:
                    out_txt.write(bracken_dict[bracken_k][0]+"\t"+bracken_k+"\t"+bracken_dict[bracken_k][1]+"\t"
                                  + bracken_dict[bracken_k][2]+"\t"+bracken_dict[bracken_k][3]+"\t"
                                  +bracken_dict[bracken_k][4]+"\t"+bracken_dict[bracken_k][5]+"\t"+"\n")
    out_txt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("filter info from xls")
    parser.add_argument("-x","--xls_file",type=str,help="*.xls file")
    parser.add_argument("-t", "--txt_file", type=str, help="*.txt file")
    parser.add_argument("-p", "--path", type=str, help="*.txt file path or output file path "
                                                       "such as /home/pmd/analysis/PM19436/se_v1/R191217OTPN016/bracken")
    args = parser.parse_args()
    cur_path = os.getcwd()
    xls_taxid = []
    bracken_dict = {}
    filter_info(cur_path,xls_taxid,bracken_dict)
