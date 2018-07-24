# -*- coding: utf-8 -*-
import telnetlib
import time
import paramiko
import re
import xlrd
import os
import threading

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
        """根据简道云导出的输入文件input.xlsx备份交换机信息"""
        dev_list = []
        input_data = xlrd.open_workbook(path)  # '/Users/huaqiang/Downloads/input.xlsx')
        table = input_data.sheets()[0]
        row_count = table.nrows
        col_count = table.ncols
        for index in range(0, col_count):
            # print(table.row_values(0)[index])
            if table.row_values(0)[index].encode() == '站点名称'.encode():
                site_name_num = index
            if table.row_values(0)[index].encode() == 'WAN IP'.encode():
                wan_ip_num = index
            if table.row_values(0)[index].encode() == 'LAN IP'.encode():
                lan_ip_num = index
            if table.row_values(0)[index].encode() == '防火墙下一跳'.encode():
                nexthop_num = index
            if table.row_values(0)[index].encode() == 'loopback'.encode():
                loopback_num = index
                    # print(site_name_num,lan_ip_num)
                # print(site_name_num,lan_ip_num)
        for index in range(1, row_count):
            dev_info = {
                'Site_name': table.row_values(index)[site_name_num],
                'WAN_IP': table.row_values(index)[wan_ip_num],
                'LAN_IP': table.row_values(index)[lan_ip_num],
                'Nexthop': table.row_values(index)[nexthop_num],
                'loopback': table.row_values(index)[loopback_num]
            }
            dev_list.append(dev_info)
        return dev_list

class NetworkMgmt(object):
    """ for networks devices & functions """

    def __init__(self, host, usr, pwd):
        self.host = host
        self.usr = usr
        self.pwd = pwd
        # self.cmd_list = cmd_list

    def telnet_run(self, cmd_list, prompt_usr='Username:', prompt_pwd='Password:', prompt_ena='>',
                   prompt_conf=']', timeout=2, LOGIN_LOG=0):
        """
        telnet and run cmd_list

        Parameters:
            LOGIN_LOG - include login log or not
            prompt_usr -
            prompt_pwd -
            prompt_ena -
            prompt_conf -

        Returns:
            screen_buffer - as the name told u.
            result - a list include the result info.
            {'host', 'conn_type': [telnet, ssh, fail], 'result': 1 or 0}

        Raises:

        """
        prompt_usr = prompt_usr.encode("ascii")
        prompt_pwd = prompt_pwd.encode("ascii")
        prompt_ena = prompt_ena.encode("ascii")
        prompt_conf = prompt_conf.encode("ascii")
        screen_buffer = {'host': self.host}
        log_sleep_time = 1
        output = ''
        try:
            tn = telnetlib.Telnet(self.host, port=23, timeout=1)
        except:
            screen_buffer = 'none'
            result = {'host': self.host, 'conn_type': 'telnet', 'result': 0, 'screen_buffer': screen_buffer}
            return result
        else:
            # login
            #   username info
            if LOGIN_LOG:
                # time.sleep(log_sleep_time)
                output = output + tn.read_until(prompt_usr, timeout).decode('ascii')
            else:
                tn.read_until(prompt_usr, timeout)
            tn.write(self.usr.encode("ascii") + b'\n')
            #   password info
            if self.pwd:
                if LOGIN_LOG:
                    output = output + tn.read_until(prompt_pwd, timeout).decode('ascii')
                else:
                    tn.read_until(prompt_pwd, timeout)
                tn.write(self.pwd.encode("ascii") + b'\n')
            else:
                tn.read_until(prompt_pwd, timeout)
                tn.write(b'\n')
            # login info
            if LOGIN_LOG:
                # time.sleep(log_sleep_time)
                output = output + tn.read_until(prompt_ena, timeout).decode('ascii')
            else:
                tn.read_until(prompt_ena, timeout + 1)
                tn.write(b'\n')  # make the first command in prompt
            # run cmd_list
            for cmd in cmd_list:
                tn.write(cmd.encode("ascii") + b'\n')
                time.sleep(0.5)
                output = output + tn.read_very_eager().decode('ascii')
                # tn.read_until(prompt_conf, timeout)

            screen_buffer = output
            tn.close()

            result = {'host': self.host, 'conn_type': 'telnet', 'result': 1, 'screen_buffer': screen_buffer}
            return result


def cfg(host):
    fw_wan = host['WAN_IP']
    fw_lan = host['LAN_IP']
    fw_nexthop = host['Nexthop']
    loopback0 = host['loopback']
    cmd_list = [
        'sys',
        'ospf 10',
        'area 0.0.0.35',
        'netw  ' + fw_wan + ' 0.0.0.3',
        'netw  ' + fw_lan + ' 0.0.0.7',
        'undo nqa entry unis 1',
        'undo nqa entry unis 2',
        'nqa entry unis 1',
        ' type icmp-echo',
        '  description loopback-to-server',
        '  destination ip 172.16.8.17',
        '  frequency 30000',
        '  probe count 5',
        '  source ip  ' + loopback0,
        '#',
        'nqa entry unis 2',
        ' type icmp-echo',
        '  description jieshouji-to-server',
        '  destination ip 172.16.8.19',
        '  frequency 30000',
        '  probe count 5',
        '  source ip ' + fw_lan,
        '#',
        'nqa entry unis 3',
        ' type icmp-echo',
        '  description loopback-to-SHTL',
        '  destination ip 172.18.0.72',
        '  frequency 30000',
        '  probe count 5',
        '  source ip ' + loopback0,
        '#',
        'nqa entry unis 4',
        ' type icmp-echo',
        '  description jieshouji-to-SHTL',
        '  destination ip 172.18.0.72',
        '  frequency 30000',
        '  probe count 5',
        '  source ip ' + fw_lan,
        ' #',
        ' nqa schedule unis 1 start-time now lifetime forever',
        ' nqa schedule unis 2 start-time now lifetime forever',
        ' nqa schedule unis 3 start-time now lifetime forever',
        ' nqa schedule unis 4 start-time now lifetime forever',
        'Acl adv 3000',
        'Rule 7 per ospf',
        'Acl adv 3001',
        'Rule 7 per ospf ',
        'Int gi0/0',
        'Ospf netw p2p ',
        'policy-based-route loopback permit node 5',
        ' if-match acl 2010',
        ' apply output-interface Eth-channel1/0:0',
        '#',
        'ip local policy-based-route loopback',
        'acl basic 2010',
        'rule 5 permit source ' + loopback0 + ' 0',
        'undo ntp-service source',
        'undo ntp-service unicast-server 172.16.25.4',
        '#',
        ' ntp-service enable',
        ' ntp-service unicast-server 172.16.64.29 source LoopBack0',
        ' clock timezone PRC add 08:00:00',
        '#',
        'scheduler job ping',
        ' command 1 ping -a ' + loopback0 + ' -c 5 172.16.8.17',
        '#',
        'scheduler schedule ping',
        ' user-role network-admin',
        ' job ping',
        ' time repeating interval 15',
        ' undo user-role network-operator ',
        '#',
        '#',
        'rtm cli-policy eaa-check',
        ' event syslog priority 6 msg PING/6/PING_STATISTICS.*172.16.8.17.*100.0%.*loss occurs 1 period 3',
        ' action 0 cli system-view',
        ' action 1 cli controller cellular 1/0',
        ' action 2 cli modem reboot',
        " action 3 syslog priority 4 facility local3 msg 'EAA modem reboot Occurred!'",
        ' user-role network-admin',
        ' undo user-role network-operator',
        ' commit',
        '#',
        'ip route-static 117.131.57.38 32 Eth-channel1/0:0',
        'ip route-static 117.185.39.254 32 Eth-channel1/0:0',
        'undo ip route-static 0.0.0.0 0 ' + fw_nexthop,
        '# save force'
    ]
    a = NetworkMgmt(host=host['WAN_IP'], usr='admin', pwd='Admin@123')
    result = a.telnet_run(prompt_usr='login:', prompt_pwd='Password:', cmd_list=cmd_list)
    return result


def cfg_distributor(host_list):
    for host in host_list:
        # print(host)
        txt = cfg(host)['screen_buffer']
        if txt == 0:
            result = 'Failed'
        else:
            result = 'OK'
        print(host['Site_name'], '\t', host['WAN_IP'], '\t', result)
        with open('./run_result/' + host['Site_name'] + '-' + host['WAN_IP'] +  '.log', 'w', encoding='utf-8') as f:
            f.write(txt)


def main():
    start = time.time()
    path = '/ops/NetMgmt/'
    test_path = '/Users/huaqiang/Downloads/hainan_4G.xlsx'
    threadpool = []
    m = Util()
    dev_list = m.get_dev_list(path + 'input_file/hainan_4G.xlsx')
    # dev_list = m.get_dev_list(test_path)
    m.multi_task(cfg_distributor, dev_list, n=30)
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()