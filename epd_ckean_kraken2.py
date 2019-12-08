#_*_coding:UTF-8_*_
import os
import subprocess
import argparse


def kraken_verificate_epd(kraken_path,kraken_edp_index,bracken_path,cur_path):

    # kraken
    cmd = kraken_path + " --db " + kraken_edp_index  \
          + " --gzip-compressed --threads 8 --report-zero-counts --confidence 0.65 --report " \
          + cur_path + "/" + args.sample_num + ".epd.kraken.report.txt" \
          + " --classified-out " + cur_path + "/" + args.sample_num + ".epd.fastq.gz" \
          + " --use-names " + "/home/pmd/analysis/" + args.batch + "/se_v1/" \
          + args.sample_num + "/map/" + args.sample_num + ".non_human.exclude.fastq.gz" \
          + " > " + cur_path + "/" + args.sample_num + ".epd.kraken.out.txt"
    subprocess.check_output(cmd, shell=True)

    # bracken
    # species
    cmd1 = "python " + bracken_path + " -k /pmd/Genome/fungi/kraken_eupathDB/database75mers.kmer_distrib -t 1  -l S -i " \
           + cur_path + "/" + args.sample_num + ".epd.kraken.report.txt" \
           + " -o " + cur_path + "/" + args.sample_num + ".epd.bracken.species.txt"
    # genus
    cmd2 = "python " + bracken_path + " -k /pmd/Genome/fungi/kraken_eupathDB/database75mers.kmer_distrib -t 1  -l G -i " \
           + cur_path + "/" + args.sample_num + ".epd.kraken.report.txt" \
           + " -o " + cur_path + "/" + args.sample_num + ".epd.bracken.genus.txt"
    subprocess.check_output(cmd1, shell=True)
    subprocess.check_output(cmd2, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("eupathdb verification")
    parser.add_argument("-b", "--batch", type=str, help="batch, as 'PM19408' ")
    parser.add_argument("-s", "--sample_num", type=str, help="sample number")
    # parser.add_argument("-t", "--taxid", type=str, help="taxid as '5059' ")
    args = parser.parse_args()
    cur_path = os.getcwd()
    kraken_path = "/data1/soft/kraken2/kraken2/kraken2"
    kraken_edp_index = "/pmd/Genome/fungi/kraken_eupathDB"
    bracken_path = "/data1/share/bin/Bracken-2.2/src//est_abundance.py"
    kraken_verificate_epd(kraken_path,kraken_edp_index,bracken_path,cur_path)