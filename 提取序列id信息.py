#_*_coding:UTF-8_*_
import gzip

def read_fastq(ids):
    NR = 0
    with gzip.open(r"D:\My Projects\01_test\SRR8578913_1.fastq.gz", "rb") as input_file:
        for line in input_file:
            while NR < 100:
                if NR % 4 == 0:
                    ids.append(line.decode().strip("\n"))
                else:
                    pass
                NR += 1
    input_file.close()


def write_id(ids):
    with open(r"D:\My Projects\01_test\seq_id.txt", "w") as output_file:
        for id in ids:
            output_file.write(id + "\n")
    output_file.close()


def main():
    ids = []
    read_fastq(ids)
    write_id(ids)

if __name__ == "__main__":
    main()
