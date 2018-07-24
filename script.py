import time

import xlrd

from scripts.modules import Station


def get_sn():
    host_list = []
    file_url = '/Users/huaqiang/Downloads/'  # 设置默认目录
    with open(file_url + '20161209065019-result.txt', 'r') as f:
        for line in f:
                host_list.append(line)
    f.close()
    result = []
    n = 0
    for host_str in host_list:
        host = host_str.replace('\n','')
        n += 1
        print(n)
        a = SwitchMgmt(host)
        result.append(a.run())
    print(result)
    with open(file_url + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '-result.txt', 'w') as f:
        f.write(str(result))
    input('Done.')



def backup_sw_config():
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    tftp_server = '172.16.64.3'
    input_data = xlrd.open_workbook('./input.xlsx')
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
    for index in range(1, row_count):
        dev_info = {
            'Dev_name': table.row_values(index)[dev_name_num],
            'IP': table.row_values(index)[ip_name_num]
        }
        dev_list.append(dev_info)
    print(dev_list)
    for device in dev_list:
        host = device['IP']
        device_name = device['Dev_name']
        m = SwitchMgmt(host, 'admin', 'Admin@123', command='save force')
        m.ssh_run()
        command = 'tftp ' + tftp_server + ' put startup.cfg ' + host + '-' \
                  + time.strftime('%Y%m%d%S', time.localtime(time.time()))
        # print(command)
        m = SwitchMgmt(host, 'admin', 'Admin@123', command=command)
        backup_result = m.ssh_run()
        print(backup_result)


def main():
    switch_config('/Users/huaqiang/Downloads/host.xlsx')
    #host_monitor('/Users/huaqiang/Downloads/host.xlsx')




if __name__ == '__main__':
    main()