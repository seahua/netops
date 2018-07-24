# -*- coding: utf-8 -*-
# ver 1.0  2017/1/3

import threading
import time

import xlrd

from scripts.modules import NetDevMgmt

info_list = []

def device_info():
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook('/ops/NetMgmt/sw-input.xlsx') # './input.xlsx')
    table = input_data.sheets()[0]
    row_count = table.nrows
    col_count = table.ncols
    for index in range(0, col_count):
        # print(table.row_values(0)[index])
        if table.row_values(0)[index].encode() == '设备名称'.encode():
            dev_name_num = index
        if table.row_values(0)[index].encode() == '管理IP'.encode():
            ip_name_num = index
    # print(dev_name_num,ip_name_num)
    for index in range(1, row_count):
        dev_info = {
            'Dev_name': table.row_values(index)[dev_name_num],
            'IP': table.row_values(index)[ip_name_num]
        }
        dev_list.append(dev_info)
    return dev_list



def get_version_info(dev_list):
    for device in dev_list:
        host = device['IP']
        device_name = device['Dev_name']
        try:
            m = NetDevMgmt(host,'admin','Admin@123', command_list=['display version'])
            get_info_result = m.ssh_run()
            info = {'Dev_name': device_name,
                    'IP': host,
                    'info': get_info_result
                    }
            info_list.append(info)
        except:
            print("can't connect to host " + host + ' ' + device_name)

def main():
    start = time.time()
    threadpool = []
    dev_list = device_info()
    count = len(dev_list) - 1
    m = count - 5
    while count > 5:
        n = count
        m = count - 5
        count -= 5
        #print(n,m)
        backup_list = dev_list[m:n]
        th = threading.Thread(target=get_version_info,args=(backup_list,))
        threadpool.append(th)
    backup_list = dev_list[0:m]
    th = threading.Thread(target=get_version_info,args=(backup_list,))
    threadpool.append(th)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)

    with open('./version_info.txt', 'w', encoding='utf-8') as f:
        f.write(str(info_list))

    end = time.time()
    print(end - start)




if __name__ == '__main__':
    main()
