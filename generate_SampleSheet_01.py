#_*_coding:UTF-8_*_
import xlrd
import csv
import datetime
# import pandas as pd

def read_excel(lib_and_index_info):
    pooling_file = xlrd.open_workbook(r"D:\My Projects\Pooling任务单-GR190335-20191002.xlsx", "r")
    table = pooling_file.sheet_by_name("Sheet1")
    n_rows = table.nrows  # 获取行数
    # lib_and_index_info = {}  # 新建字典存储实验室编号以及index序列信息 键为实验室编号信息，值为index信息
    for i in range(5, n_rows):  # pooling表的第5行开始为实验室记录的文库及index取样等信息的表头
        lib_num = table.cell(i, 1).value.strip()
        index_info = table.cell(i, 3).value.strip()
        # 如果单元格中有空白行或者只有一个cell有数据的删除
        lib_and_index_info[lib_num] = index_info  # 生成样本编号与index对应关系的字典
        if index_info == "":  # 判断index中信息是否为空值
            lib_and_index_info.pop(lib_num)  # 删除值为空的键，即从字典中删除了该信息


def read_index_seq(index_dict):
    # index_dict = {}
    """
    出于测序模式的选择（76+6+6+1和76+8+8+1）两种模式的选择，
    增加了对index碱基数的if判断，在调用该脚本是写入使用的是8或者6碱基的模式，
    生成满足6碱基或者8碱基的index序列
    :param index_dict:
    :return: None
    """
    index_num = int(input("输入index的碱基数： "))  # 数值类型转换
    # index_num = input("输入index的碱基数： ")  # 该命令直接执行else后的语句
    with open(r"D:\My Projects\DoubleIndex.txt", "r") as index_file:
        if index_num == 8:
            for i in range(1, 96):
                lines = index_file.readline()
                index_name = lines.split("\t")[0]
                P7_seq = lines.split("\t")[2]
                P5_seq = lines.split("\t")[4]
                index_dict[index_name] = [P7_seq, P5_seq]
        else:
            for i in range(1, 96):
                lines = index_file.readline()
                index_name = lines.split("\t")[0]
                P7_seq = lines.split("\t")[2][:6]
                P5_seq = lines.split("\t")[4][:6]
                index_dict[index_name] = [P7_seq, P5_seq]
    index_file.close()


def write_csv(lib_and_index_info,index_dict):
    global write_sam_num
    write_sam_num = 0
    current_time = datetime.datetime.now().strftime('%Y/%m/%d')
    with open(r"D:\My Projects\SampleSheet.csv", "w", newline="") as temp_csv:  # newline=""控制行距，经测试只可在python3环境下使用
        csv_writer = csv.writer(temp_csv)
        csv_writer.writerow(["[Header]"])
        csv_writer.writerow(["IEMFileVersion", 4])
        csv_writer.writerow(["Experiment Name", "batch"])  # 通过输入传入批次号参数
        csv_writer.writerow(["Date", current_time])  # 通过datetime获取当前时间，并规定其格式（yy/mm/dd）
        csv_writer.writerow(["Workflow", "GenerateFASTQ"])
        csv_writer.writerow(["Application", "NextSeq FASTQ Only"])
        csv_writer.writerow(["Assay", "TruSeq LT"])
        csv_writer.writerow(["Description"])
        csv_writer.writerow(["Chemistry", "Default"])
        csv_writer.writerow([])
        csv_writer.writerow(["[Reads]"])
        csv_writer.writerow([76])
        csv_writer.writerow([76])
        csv_writer.writerow([])
        csv_writer.writerow(["[Settings]"])
        csv_writer.writerow(["Adapter"])
        csv_writer.writerow(["AdapterRead2"])
        csv_writer.writerow([])
        csv_writer.writerow(["[Data]"])
        col_names = ["Sample_ID", "Sample_Name", "Sample_Plate", "Sample_Well",
                     "I7_Index_ID", "index", "index2","Sample_Project", "Description"]  # 表头信息
        csv_writer = csv.DictWriter(temp_csv, fieldnames=col_names)  # 添加表头信息，用于构建字典
        csv_writer.writeheader()
        for k_lib, v_lib in lib_and_index_info.items():
            for k_index, v_index in index_dict.items():
                if v_lib == k_index:
                    # index_P7 = v_index[0]
                    # index_P5 = v_index[1]
                    csv_writer.writerow(
                        {"Sample_ID": k_lib, "Sample_Name": k_lib, "I7_Index_ID": v_lib, "index": v_index[0],
                         "index2": v_index[1], "Sample_Project": "fastq", "Description": "fastq"})
                    write_sam_num += 1
        temp_csv.close()
        return write_sam_num


def judge(lib_and_index_info):
    # 判断从excel文件中读取数据的数量和写入csv文件中的数量是否一致
    if write_sam_num == len(lib_and_index_info):  # 增加判断写入的数据和读取的数据个数是否一致
        print("Numbers of sample to be analyzed:{}".format(len(lib_and_index_info)))
    else:
        print("Please check the sample information of the output file：Inconsistent results")


# def error():
#     try:
#         pass
#     except:
#         pass

def main():  # 主函数
    lib_and_index_info = {}
    index_dict = {}
    read_excel(lib_and_index_info)
    read_index_seq(index_dict)
    write_csv(lib_and_index_info,index_dict)
    judge(lib_and_index_info)

    # 异常处理
    # if write_sam_num == len(lib_and_index_info):  # 增加判断写入的数据和读取的数据个数是否一致
    #     print("Numbers of sample to be analyzed:{}".format(len(lib_and_index_info)))
    # else:
    #     print("Please check the sample information of the output file：Inconsistent results")

if __name__ == "__main__":
    main()