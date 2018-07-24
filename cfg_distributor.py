# -*- coding: utf-8 -*-
# ver 1.0  2017/1/12

import threading
import time

import xlrd

from scripts.modules import NetDevMgmt


def get_dev_list():
    """根据简道云导出的输入文件input.xlsx获得交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook('/Users/huaqiang/Downloads/input.xlsx')
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


def cfg_distribute(dev_list):
    for device in dev_list:
        host = device['IP']
        device_name = device['Dev_name']
        command_list = ['sys', 'sflow agent ip ' + host,
                        'sflow collector 1 ip 172.16.192.1 description to-sflowcollector',
                        'interface GigabitEthernet1/0/3', ' sflow flow collector 1', ' sflow sampling-rate 5000',
                        ' sflow counter collector 1', ' sflow counter interval 30', 'return', 'save force']
        try:
            m = NetDevMgmt(host, 'admin', 'Admin@123', command_list=command_list)
            backup_result = m.ssh_run()
            print(backup_result)
        except:
            print("can't connect to host " + host + ' ' + device_name)


def main():
    start = time.time()
    threadpool = []
    dev_list = get_dev_list()
    count = len(dev_list)
    m = count
    while count > 5:
        n = count - 1
        m = count - 6
        count -= 5
        #print(n,m)
        backup_list = dev_list[m:n]
        th = threading.Thread(target=cfg_distribute,args=(backup_list,))
        threadpool.append(th)
    backup_list = dev_list[0:m]
    th = threading.Thread(target=cfg_distribute,args=(backup_list,))
    threadpool.append(th)

    for th in threadpool:
        th.start()

    for th in threadpool:
        threading.Thread.join(th)

    end = time.time()
    print(end - start)

if __name__ == '__main__':
    main()