# -*- coding: utf-8 -*-
# ver 1.0  -- 2017/1/3 --
# ver 2.0  -- 2017/10/25 --
# ver 2.1  -- 2017/10/27 --

import telnetlib
import time
import paramiko
import re
import xlrd
import os
from IPy import IP


class Network(object):
    """ for networks devices & functions """
    def __init__(self, host, usr, pwd):
        self.host = host
        self.usr = usr
        self.pwd = pwd
        # self.cmd_list = cmd_list

    def telnet_run(self, cmd_list, prompt_usr='Username:', prompt_pwd='Password:', prompt_ena='>',
                   prompt_conf=']', timeout=2, login_log=0):
        """
        telnet and run

            login_log : 是否需要login日志
            prompt_usr : 识别登陆后的用户名提示符
            prompt_pwd : 识别登陆后的密码提示符
            prompt_ena : enable模式识别符
            prompt_conf : conf模式识别符
            cmd_list :  运行命令清单
            timeout : 单条命令超时时间
            
        Returns:
            screen_buffer - 屏幕输出日志
            result - 一个包含输出日志的list：
            {'host', 'conn_type': [telnet, ssh], 'result': 1 or 0, 'screen_buffer'}
        """
        prompt_usr = prompt_usr.encode("ascii")
        prompt_pwd = prompt_pwd.encode("ascii")
        prompt_ena = prompt_ena.encode("ascii")
        prompt_conf = prompt_conf.encode("ascii")
        # screen_buffer = {'host': self.host}
        # log_sleep_time = 1
        output = ''
        try:
            tn = telnetlib.Telnet(self.host, port=23, timeout=1)
        except:
            screen_buffer = output
            result = {'host': self.host, 'conn_type': 'telnet', 'result': 0, 'screen_buffer':screen_buffer}
            return result
        else:
            #   login
            #   username info
            if login_log:
                # time.sleep(log_sleep_time)
                output = output + tn.read_until(prompt_usr, timeout).decode('ascii')
            else:
                tn.read_until(prompt_usr, timeout)
            tn.write(self.usr.encode("ascii") + b'\n')
            #   password info
            if self.pwd:
                if login_log:
                    output = output + tn.read_until(prompt_pwd, timeout).decode('ascii')
                else:
                    tn.read_until(prompt_pwd, timeout)
                tn.write(self.pwd.encode("ascii") + b'\n')
            else:
                tn.read_until(prompt_pwd, timeout)
                tn.write(b'\n')
            # login info
            if login_log:
                # time.sleep(log_sleep_time)
                output = output + tn.read_until(prompt_ena, timeout).decode('ascii')
            else:
                tn.read_until(prompt_ena, timeout + 1)
                tn.write(b'\n')  # make the first command in screen_buffer
            # run cmd_list
            for cmd in cmd_list:
                tn.write(cmd.encode("ascii") + b'\n')
                time.sleep(0.5)
                output = output + tn.read_very_eager().decode('ascii')
                # tn.read_until(prompt_conf, timeout)
            screen_buffer = output
            tn.close()

            result = {'host': self.host, 'conn_type': 'telnet', 'result': 1, 'screen_buffer':screen_buffer}
            return result

    def ssh_run(self, cmd_list, timeout=1):
        """
        ssh and run cmd_list
        cmd_list :  运行命令清单
        timeout : 单条命令超时时间

        Returns:
        screen_buffer - 屏幕输出日志
        result - 一个包含输出日志的list：
        {'host', 'conn_type': [telnet, ssh], 'result': 1 or 0, 'screen_buffer'}
        """
        # screen_buffer = {'host': self.host}
        ssh_pre = paramiko.SSHClient()
        ssh_pre.load_system_host_keys()
        ssh_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_pre.connect(self.host,username=self.usr,
                        password=self.pwd, look_for_keys=False, allow_agent=False, timeout=3)
        except:
            screen_buffer = ''
            result = {'host': self.host, 'conn_type': 'ssh', 'result': 0, 'screen_buffer':screen_buffer}
            return result
        else:
            # Use invoke_shell to establish an 'interactive session'
            ssh = ssh_pre.invoke_shell()
            ssh.settimeout(5)
            # output = ssh.recv(450)
            # print(str(output,'utf-8'))
            time.sleep(timeout)
            # run cmd_list
            for command in cmd_list:
                ssh.send(command + '\n')
                time.sleep(timeout)
                # print(str(ssh.recv(1000), 'utf-8'))
            screen_buffer = str(ssh.recv(100000),'utf-8')
            ssh.close()

            result = {'host': self.host, 'conn_type': 'ssh', 'result': 1, 'screen_buffer': screen_buffer}
            return result

    def get_fw_brand(self):
        """
        根据login banner返回防火墙品牌信息
        """
        # 获取登录banner
        try:
            tn = telnetlib.Telnet(self.host, port=23, timeout=3)
        except:
            return '404'
        else:
            tn.read_until(b" ",2)
            screen_buffer = tn.read_very_eager().decode('ascii')
            tn.close()
            # 解析关键字获取品牌信息
            if screen_buffer.find('Huawei') > 0:
                return 'Huawei'
            elif screen_buffer.find('H3C') > 0:
                return 'H3C'
            elif screen_buffer.find('Unis') > 0:
                return 'Unis'
            else:
                return 'Other'