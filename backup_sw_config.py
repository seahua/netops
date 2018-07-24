# -*- coding: utf-8 -*-
# ver 1.0  2017/1/3

import threading
import time

import xlrd

from scripts.modules import NetDevMgmt


def backup_info():
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook('/Users/huaqiang/Downloads/input.xlsx') # './input.xlsx')
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



def backup_sw_config(dev_list):
    tftp_server = '172.16.64.3'
    for device in dev_list:
        host = device['IP']
        device_name = device['Dev_name']
        try:
            m = NetDevMgmt(host,'admin','Admin@123', command_list=['save force'])
            m.ssh_run()
            command = 'tftp ' + tftp_server + ' put startup.cfg ' + device_name + '-' + host +'-' \
                  + time.strftime('%Y%m%d%S', time.localtime(time.time()))
           # print(host,device_name)
            m = NetDevMgmt(host, 'admin', 'Admin@123', command_list=command)
            backup_result = m.ssh_run(4)
            print(backup_result)
        except:
            print("can't connect to host " + host + ' ' + device_name)

def main():
    start = time.time()
    threadpool = []
    dev_list = backup_info()
    count = len(dev_list) - 1
    m = count - 5
    while count > 5:
        n = count
        m = count - 5
        count -= 5
        #print(n,m)
        backup_list = dev_list[m:n]
        th = threading.Thread(target=backup_sw_config,args=(backup_list,))
        threadpool.append(th)
    backup_list = dev_list[0:m]
    th = threading.Thread(target=backup_sw_config,args=(backup_list,))
    threadpool.append(th)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    main()