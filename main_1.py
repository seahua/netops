# -*- coding: utf-8 -*-

import xlrd

from scripts.modules import SwitchMgmt


def backup_sw_config():
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook('/Users/huaqiang/Downloads/input.xlsx')
    table = input_data.sheets()[0]
    row_count = table.nrows
    col_count = table.ncols
    for index in range(0,col_count):
        # print(table.row_values(0)[index])
        if table.row_values(0)[index].encode() == '设备名称'.encode():
            dev_name_num = index
        if table.row_values(0)[index].encode() == '管理IP'.encode():
            ip_name_num = index
    # print(dev_name_num,ip_name_num)
    for index in range(1,row_count):
       dev_info = {
           'Dev_name':table.row_values(index)[dev_name_num],
           'IP':table.row_values(index)[ip_name_num]
       }
       dev_list.append(dev_info)
    print(dev_list)
    for device in dev_list:
        host = device['IP']
        device_name = device['Dev_name']
        m = SwitchMgmt(host,'admin','Admin@123',command='save force')
        m.ssh_run()
        command = 'tftp ' + host + ' put startup.cfg ' + host +'-' \
              + time.strftime('%Y%m%d%S', time.localtime(time.time()))
        # print(command)
        m = SwitchMgmt(host, 'admin', 'Admin@123',command=command)
        backup_result = m.ssh_run()
        print(backup_result)

def main():
    backup_sw_config()

if __name__ == '__main__':
    main()