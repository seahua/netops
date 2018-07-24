import re
import time
import xlrd
import os
from IPy import IP


class Station(object):
    """
    交换机脚本及hostmonitor脚本输入文件：host.xlsx
    输入表头：站点名称 | 站点名拼音 | 站点IP | 防火墙ip | VLAN
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.dirname = os.path.dirname(self.input_file)
        self.pardir = os.path.abspath(os.path.join(self.dirname, os.path.pardir))

    def _get_site_list(self):
        """
        获取host.xlsx的信息
        :rtype [[site_name, spell, host, wan_ip, vlan] ...]
        """
        site_list = []
        input_data = xlrd.open_workbook(self.input_file)
        # table = input_data.sheets()[0]
        table = input_data.sheet_by_name('station')
        row_count = table.nrows
        for i, item in enumerate(table.row_values(0)):
            if item == '站点名称':
                site_name_col = i
            if item == '站点名拼音':
                spell_col = i
            if item == '站点IP':
                host_col = i
            if item == '防火墙IP':
                wan_ip_col = i
            if item == 'Vlan':
                vlan_col = i
        # column heading
        data = table.row_values(0)
        host = [data[site_name_col], data[spell_col], data[host_col], data[wan_ip_col], data[vlan_col]]
        site_list.append(host)
        # site info
        for row_num in range(1, row_count):
            data = table.row_values(row_num)
            host = [data[site_name_col], data[spell_col], data[host_col], data[wan_ip_col], int(data[vlan_col])]
            site_list.append(host)

        return site_list

    def get_hostmonitor_script(self, FW = 1):
        """

        :return: file path
        """
        host_list = self._get_site_list()
        file = self.pardir + '/results/' + time.strftime('%Y%m%d%H%M%S-', time.localtime(time.time())) + 'hostmonitor.txt'
        for host in host_list[1:]:
            fw_monitor_script = ('Method      = Ping\nTitle       = afw-' + host[0] +
                                 '\nInterval    = 60\nHost        = ' + host[3] +
                                 '\nTimeout     = 3000\nRetries     = 4\nMaxLostRatio= 90\nDisplayMode = received\n')
            bs_monitor_script = ('Method      = Ping\nTitle       = ' + host[0] +
                                 '\nInterval    = 60\nHost        = ' + host[2] +
                                 '\nTimeout     = 3000\nRetries     = 4\nMaxLostRatio= 90\nDisplayMode = received\n')

            with open(file, 'a', encoding='GBK') as f:
                f.write(bs_monitor_script)
                if FW:
                    f.write(fw_monitor_script)
        return file

    def get_switch_script(self):
        """

        :return: file path
        """
        host_list = self._get_site_list()
        file = self.pardir + '/results/' + time.strftime('%Y%m%d%H%M-', time.localtime(time.time())) + 'switch.txt'
        for host in host_list[1:]:
            fw_ip = host[3]
            sw_ip = str(IP(IP(fw_ip).net().int() - 1))
            vlan = str(host[4])
            spell = host[1]
            bs_ip = host[2]

            sw_script = ('vlan ' + vlan + '\n' +
                         'interface Vlan' + vlan + '\n' +
                         ' description ' + spell + '\n' +
                         ' ip address ' + sw_ip + ' 30\n' +
                         'ip rout ' + bs_ip + ' 29 ' + fw_ip + ' description ' + spell + '\n' +
                         '#\n')

            with open(file, 'a', encoding='utf-8') as f:
                f.write(sw_script)

            return file

