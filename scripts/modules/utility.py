# -*- coding: utf-8 -*-
# ver 1.0  -- 2017/11/6 --

import threading
import time
import xlrd
import xlsxwriter


class Util(object):
    """None"""
    def __init__(self):
        None

    def list_split(self, l1, n=1):
        """
        split l1 = [a1, a2, a3, a4, a5], n = 2
        return l2 = [[a1, a2], [a3, a4], [a5]]
        """
        if (len(l1) % n) == 0:
            m = len(l1) // n
        else:
            m = len(l1) // n + 1
        l2 = [l1[i * n:(i + 1) * n] for i in range(m)]
        return l2

    def multi_task(self, obj, arg_list, n=1):
        """type(arg_list) == list"""
        threadpool = []
        a = Util()
        arg_list = a.list_split(arg_list, n)
        for sub_arg_list in arg_list:
            # print(sub_arg_list)
            th = threading.Thread(target=obj, args=(sub_arg_list,))
            threadpool.append(th)
        for th in threadpool:
            th.start()
        for th in threadpool:
            threading.Thread.join(th)

    def get_dev_list(self, path):
        """
        根据CMDB导出的输入文件input.xlsx获取设备list
        """
        dev_list = []
        input_data = xlrd.open_workbook(path) #'/Users/huaqiang/Downloads/input.xlsx')
        table = input_data.sheets()[0]
        row_count = table.nrows
        col_count = table.ncols
        for index in range(0, col_count):
            # print(table.row_values(0)[index])
            if table.row_values(0)[index].encode() == '站点名称'.encode():
                site_name_num = index
            if table.row_values(0)[index].encode() == '防火墙/路由器-LAN'.encode():
                lan_ip_num = index
        # print(site_name_num,lan_ip_num)
        for index in range(1, row_count):
            dev_info = {
                'Site_name': table.row_values(index)[site_name_num],
                'IP': table.row_values(index)[lan_ip_num]
            }
            dev_list.append(dev_info)
        return dev_list


def get_brand(dev_list):
    """none"""
    brand_name = 'Null'
    for device in dev_list:
        #brand = NetDevMgmt(host=device['IP'], usr='', pwd='').get_fw_brand()
        if brand == 2:
            brand_name = 'Huawei'
        if brand == 1:
            brand_name = 'H3C'
        if brand == 0:
            brand_name = 'Sangfor'

        brand_info = {
            'Site_name': device['Site_name'],
            'IP': device['IP'],
            'Brand': brand_name
        }
        brand_list.append(brand_info)


def main():
    """none"""
    start = time.time()
    path = '/ops/NetMgmt/'
    threadpool = []
    dev_list = get_dev_list(path + 'input_file/input.xlsx')

    n = 10
    dev_list_new = list_spilit(dev_list, n)
    print(dev_list_new)

    for sub_dev_list in dev_list_new:
        th = threading.Thread(target=get_brand, args=(sub_dev_list,))
        threadpool.append(th)

    for th in threadpool:
        th.start()

    for th in threadpool:
        threading.Thread.join(th)

    workbook = xlsxwriter.Workbook(path + 'result/brand.xlsx')
    table = workbook.add_worksheet('brand')
    table.write(0, 0, 'Site')
    table.write(1, 0, 'IP')
    table.write(2, 0, 'Brand')

    row = 1
    for item in brand_list:
        table.write(row, 0, item['Site_name'])
        table.write(row, 1, item['IP'])
        table.write(row, 2, item['Brand'])
        row = row + 1

    workbook.close()

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()