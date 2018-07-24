# -*- coding: utf-8 -*-

import time

from modules.utility import Util

from scripts.modules.network import NetworkMgmt
from scripts.modules.network import StationMgmt


def test(l1):
    for i in l1:
        pass
        if i % 5 == 0:
            print(i)


def test_multi_task():
    cmd_list = [i for i in range(10000)]
    a = Util()
    start = time.time()
    a.multi_task(test, cmd_list, 100)
    end = time.time()
    print(end - start)


def test_ssh_run():
    cmd_list = [i for i in range(10000)]
    with open('/Users/huaqiang/Downloads/ruijie.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line != '\n':
                cmd_list.append(line.replace('\n', ''))
    host = '1.1.1.11'
    usr = pwd = 'admin'
    command_list = ['en', 'conf t']
    command_list1 = ['ip access-list standard ' + str(n) for n in range(1,201)]
    command_list.extend(command_list1)
    a = NetworkMgmt(host, usr, pwd, command_list)
    start = time.time()
    # buffer, r = a.telnet_run(prompt_ena='#', prompt_conf='#', LOGIN_LOG=1)
    # buffer, r = a.ssh_run(timeout=0.5)
    #l2 = a.list_split(2)
    end = time.time()
    print(end - start)


def test_ssh_run():
    cmd_list = ['ter len 0', 'show ver', 'show run']
    a = NetworkMgmt('1.1.1.1', 'admin', 'admin')
    buffer, result = a.ssh_run(cmd_list)
    print(buffer['log'])


def test_telnet_run(login_log=0):
    cmd_list = ['ter len 0', 'show ver', 'show run']
    a = NetworkMgmt('1.1.1.1', 'admin', 'admin')
    buffer, result = a.telnet_run(cmd_list, LOGIN_LOG=login_log)
    print(buffer['log'])


def test_station(input_file):
    a = 1


def host_monitor_script(input_file):
    a = StationMgmt(input_file)
    a.get_host_txt()
    a.get_hostmonitor_script()
    a.del_temp()


def switch_script(input_file):
    a = StationMgmt(input_file)
    a.get_host_txt()
    a.get_switch_script()
    a.del_temp()


def main():
    # test_multi_task()
    # test_ssh_run()
    # test_telnet_run()
    # test_station('基站网络信息表_20171120171458.xlsx')
    host_monitor_script('/Users/huaqiang/Downloads/template-1.xlsx')
    switch_script('/Users/huaqiang/Downloads/template-1.xlsx')


if __name__ == '__main__':
    main()