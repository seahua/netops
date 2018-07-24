# -*- coding: utf-8 -*-
import telnetlib
import time
import paramiko
import re
import xlrd
import os
from IPy import IP
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
            if table.row_values(0)[index].encode() == '管理IP'.encode():
                lan_ip_num = index
                # print(site_name_num,lan_ip_num)
        for index in range(1, row_count):
            dev_info = {
                'Site_name': table.row_values(index)[site_name_num],
                'IP': table.row_values(index)[lan_ip_num]
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

def get_host(file):
    host_list = []
    with open(file) as f:
        readlines = f.readlines()

    for host in readlines:
        host = host.replace('\n', '')
        host_list.append(host)

    return host_list

def get_context(host):
    cmd_list = ['screen-length disable', 'display cellular']
    a = NetworkMgmt(host=host, usr='admin', pwd='Admin@123')
    result = a.telnet_run(prompt_usr='login:', prompt_pwd='Password:', cmd_list=cmd_list)
    return result

def get_iccid(buffer):
    for line in buffer:
        if 'ICCID' in line:
            return line.replace('\n', '').replace('ICCID:', '')

def get_H3C_version_txt(host):
    cmd_list = ['sys', 'dis dev manuinfo']
    cmd_list_4G = []
    a = NetworkMgmt(host=host, usr='admin', pwd='admin')
    result = a.telnet_run(prompt_usr='Username:', prompt_pwd='Password:', cmd_list=cmd_list_4G)
    return result

def get_H3C_version_file(host_list):
    for host in host_list:
        txt = get_H3C_version_txt(host['IP'])['screen_buffer']
        print('txt>', txt)
        print('host>', host)
        with open(''.join(['./run_result/', host['IP'], '.txt']), 'w', encoding='utf-8') as f:
            f.write(txt)




result = []


def a(host_list):
    for host in host_list:
        result.append(get_context(host))

def main_1():
    start = time.time()
    path = '/ops/NetMgmt/'
    threadpool = []
    m = Util()
    dev_list = m.get_dev_list(path + 'input_file/H3C_input.xlsx')
    m.multi_task(get_H3C_version_file, dev_list, n=30)
    end = time.time()
    print(end - start)


def main_2():
    start = time.time()
    path = '/ops/NetMgmt/'
    threadpool = []
    m = Util()
    dev_list = m.get_dev_list(path + 'input_file/4.xlsx')
    m.multi_task(get_H3C_version_file, dev_list, n=30)
    end = time.time()
    print(end - start)




def main():
    icc_result = []
    input_file = './4g.txt'
    host_list = get_host(input_file)
    m = Util()
    m.multi_task(a, host_list, n=30)

    print(result)

    for i in result:
        print(i['screen_buffer'])
        # if i['result'] == 0:
        #     iccid = 0
        #     print(i['host'], '\t', iccid)
        # else:
        #     iccid = get_iccid(i['screen_buffer'])
        #     print(i['host'], '\t', iccid)


if __name__ == '__main__':
    main_1()
