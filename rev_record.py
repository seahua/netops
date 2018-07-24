# -*- coding: utf-8 -*-
# ver 1.0  2017/8/9

import threading
import time
from ftplib import FTP

import xlrd

result_list = []

def rev_info():
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook('/ops/NetMgmt/hexin-input.xlsx') # './input.xlsx')
    table = input_data.sheets()[0]
    row_count = table.nrows
    col_count = table.ncols
    for index in range(0, col_count):
        # print(table.row_values(0)[index])
        if table.row_values(0)[index].encode() == '站点名称'.encode():
            dev_name_num = index
        if table.row_values(0)[index].encode() == '接收机IP'.encode():
            ip_name_num = index
    # print(dev_name_num,ip_name_num)
    for index in range(1, row_count):
        dev_info = {
            'Dev_name': table.row_values(index)[dev_name_num],
            'IP': table.row_values(index)[ip_name_num]
        }
        dev_list.append(dev_info)
    return dev_list



def rev_ftp(rev_ip):
    ftp = FTP()  # 设置变量
    file_list = []
    # ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(rev_ip)  # 连接的ftp sever和端口
    ftp.login("ftp", "ftp")  # 连接的用户名，密码
    # bufsize = 1024  # 设置的缓冲区大小

    try:
        # sinan
        # ftp.cwd("./data/1-15min/2017221/")

        # hexin
        ftp.cwd("./File1/2017/221")

        # CHC
        # ftp.cwd("./repo/record_1/2017/221")
        ftp.dir("./",file_list.append)
        return file_list
    except:
        return []

def if_221_exist(dir):
    if len(dir)>0:
        return 1
    else:
        return 0


def get_result(dev_list):
    for dev in dev_list:
        rev_ip = dev['IP']
        is_221_exist = if_221_exist(rev_ftp(rev_ip))
        result = {
            'Dev_name': dev['Dev_name'],
            'IP': dev['IP'],
            'is_221_exist': is_221_exist
        }
        result_list.append(result)




def main():
    start = time.time()
    threadpool = []

    dev_list = rev_info()
    count = len(dev_list) - 1
    m = count - 5
    while count > 5:
        n = count
        m = count - 5
        count -= 6
        #print(n,m)
        backup_list = dev_list[m:n]
        th = threading.Thread(target=get_result,args=(backup_list,))
        threadpool.append(th)
        th = threading.Thread(target=get_result,args=([dev_list[n]],))
        threadpool.append(th)
    backup_list = dev_list[0:m]
    th = threading.Thread(target=get_result,args=(backup_list,))
    threadpool.append(th)
    th = threading.Thread(target=get_result, args=([dev_list[m]],))
    threadpool.append(th)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)

    with open('./rev_info-hexin.txt', 'w', encoding='utf-8') as f:
        f.write(str(result_list))

    for i in result_list:
        with open('rev_info-result-hexin.txt', 'w') as f:
            f.write(str(i['Dev_name']) + '\t' + str(i['IP']) + '\t' + str(i['is_221_exist']) + '\n')



    end = time.time()
    print(end - start)

if __name__ == '__main__':
    main()