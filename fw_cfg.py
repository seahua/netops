# -*- coding: utf-8 -*-

import telnetlib
import time
import xlrd
import threading



result_list = []


def telnet_run(host, usr, pwd, command_list):
    """运行指定的命令"""

    try:
        tn = telnetlib.Telnet(host, port=23, timeout=10)
        log = ''
        # 登录
        # print(tn.read_very_eager().decode('ascii'))
        tn.read_until(b'Username:')
        # if get_fw_brand == 2:
        #    tn.write(b'\n')
        tn.write(usr)
        tn.read_until(b'Password: ', 3)
        tn.write(pwd)
        tn.read_until(b'>', 1)
        tn.write(b'sys\n')
        # tn.write(b'screen-lengthisable' + b'\n')
        # screen_buffer = {'host': host}
        for command in command_list:
            tn.read_until(b']', 1)
            tn.write(command)
            time.sleep(0.2)
            output = tn.read_very_eager().decode('ascii')
            with open('./result/' + host + '.txt', 'a', encoding='utf-8') as f:
                f.write(str(output) + "\n")
        tn.close()
        return 1
    except:
        return 0


def fw_cfg_distribute(dev_list, command_list):
    """dev_list = [{'DEV_NAME':xx,'IP':yy}]"""

    # Huawei
    usr = b'admin\n'
    pwd = b'Admin@123\n'

    # H3C
    # usr = b'admin\n'
    # psw = b'admin\n'

    for device in dev_list:
        host = device['IP']
        r = telnet_run(host,usr,pwd,command_list)
        result = {
            'Dev_name': device['Dev_name'],
            'IP': device['IP'],
            'RESULT': r
        }
        result_list.append(result)


def list_spilit(l1, n):
    # len(l2)
    if (len(l1) % n) == 0:
        m = len(l1) // n
    else:
        m = len(l1) // n + 1
    l2 = [l1[i * n:(i + 1) * n] for i in range(m)]
    return l2


def get_dev_list(input_file):
    """根据简道云导出的输入文件input.xlsx获得交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook(input_file)
    table = input_data.sheets()[0]
    row_count = table.nrows
    col_count = table.ncols
    for index in range(0, col_count):
        # print(table.row_values(0)[index])
        if table.row_values(0)[index].encode() == '站点名称'.encode():
            dev_name_num = index
        if table.row_values(0)[index].encode() == 'IP'.encode():
            ip_name_num = index
    # print(dev_name_num,ip_name_num)
    for index in range(1, row_count):
        dev_info = {
            'Dev_name': table.row_values(index)[dev_name_num],
            'IP': table.row_values(index)[ip_name_num]
        }
        dev_list.append(dev_info)
    return dev_list

def main_test():
    input_file = '/Users/huaqiang/Downloads/fw_input.xlsx'
    print(get_dev_list(input_file))


def main():
    threadpool = []
    input_file = '/ops/NetMgmt/input_file/fw_huawei_input.xlsx' \
                 '_input.xlsx'
    dev_list = get_dev_list(input_file)
    # 每线程处理设备数量n
    n = 4
    # Huawei command_list
    command_list = [b"#\n",b"firewall packet-filter default permit interzone local trust direction inbound\n",b'Y\n',\
                    b"firewall packet-filter default permit interzone local trust direction outbound\n",b'Y\n',\
                    b"firewall packet-filter default deny interzone local untrust direction outbound\n",\
                    b"firewall packet-filter default permit interzone local dmz direction outbound\n",b'Y\n',b"#\n",\
                    b"ip address-set networks type object\n",\
                    b" address 1 172.17.0.0 mask 255.255.0.0 description for receiver and networks interconnection\n",\
                    b" address 2 172.19.0.0 mask 255.255.0.0 description for receiver and networks interconnection\n",\
                    b"#\n",b"ip address-set vpcserver type object\n",\
                    b" address 1 172.16.0.0 mask 255.255.0.0 description for server-farm-beijing-ali\n",\
                    b" address 2 172.20.128.0 mask 255.255.192.0 description for server-farm-beidou\n",\
                    b" address 3 172.20.192.0 mask 255.255.192.0 description for server-farm-deqing-ali\n",\
                    b" address 4 172.21.0.0 mask 255.255.0.0 description for server-farm-huadong\n",b"#\n",\
                    b"ip address-set bingqi type object\n",\
                    b" address 1 10.100.1.0 mask 255.255.255.0 description for zhongbing encryption\n",\
                    b" address 2 10.100.57.0 mask 255.255.255.0 description for zhongbing encryption\n",\
                    b" address 3 10.100.2.0 mask 255.255.254.0 description for zhongbing encryption\n",\
                    b" address 4 10.100.4.0 mask 255.255.255.0 description for zhongbing encryption\n",b"#\n",\
                    b"ip address-set natgateway type object\n",\
                    b" address 1 172.17.3.249 0 description for 4G-VPN-Gateway\n",\
                    b" address 2 172.17.3.237 0 description for 4G-VPN-Gateway\n",b"#\n",\
                    b"ip address-set network1 type object\n",\
                    b" address 1 172.17.0.0 mask 255.255.0.0 description for receiver and networks interconnection\n",\
                    b" address 2 172.19.0.0 mask 255.255.0.0 description for receiver and networks interconnection\n",\
                    b"#\n",b"ip service-set pertcp type object\n",\
                    b" servi 1 protoc tcp destination-po 8000 to 8010 descrip for backhaul data requested by spacex\n",\
                    b"#\n",\
                    b"ip service-set donghuan1 type object\n",\
                    b" servi 1 proto udp source-port 6000 to 6010 descrip for monitor traffic requested by donghuan\n",\
                    b"#\n",b"ip service-set donghuan2 type object\n",\
                    b" servi 1 protoc udp destination-po 6000 to 6010 descr for monitor traffic requested by server\n",\
                    b"#\n",b"ip service-set radius type object\n",\
                    b" service 1 protocol udp destination-port 1812 to 1813 description for aaa service\n",b"#\n",\
                    b"ip service-set donghuan3 type object\n",\
                    b" service 1 protocol tcp destination-port 12315 description for aaa service\n",b"#\n",\
                    b"policy interzone local untrust inbound\n",b" policy 1\n",\
                    b" description detecting connectivity\n",b"  action permit\n",\
                    b"  policy service service-set icmp\n",b"#\n",b" policy 2\n",\
                    b" description for management inflow\n",b"  action permit\n",\
                    b"  policy service service-set snmp\n",b"  policy service service-set http\n",\
                    b"  policy service service-set https\n",b"  policy source address-set vpcserver\n",\
                    b"  policy source address-set natgateway\n",b"  policy destination address-set networks\n",b"#\n",\
                    b" policy 3\n",b" description for remoteaccess\n",\
                    b"  action permit\n",b"  policy servic service-set telnet\n",b"  policy service service-set ssh\n",\
                    b"  policy source address-set vpcserver\n",\
                    b"  policy source address-set network1\n",\
                    b"  policy destination address-set networks\n",b"#\n",\
                    b"policy interzone local untrust outbound\n",b" policy 1\n",\
                    b" description detecting connectivity\n",b"  action permit\n",\
                    b"  policy service service-set icmp\n",b"#\n",b" policy 2\n",\
                    b" description for management-outflow\n",b"  action permit\n",\
                    b"  policy service service-set ntp\n",b"  policy service service-set snmptrap\n",\
                    b"  policy service service-set syslog\n",b"  policy service service-set tftp\n",\
                    b"  policy service service-set radius\n",b"  policy source address-set networks\n",\
                    b"  policy destination address-set vpcserver\n",b"#\n",b"policy interzone trust untrust inbound\n",\
                    b" policy 1\n",b" description for detecting connectivity\n",b"  action permit\n",\
                    b"  policy service service-set icmp\n",b"#\n",b" policy 2\n",\
                    b" description for management inflow\n",b"  action permit\n",\
                    b"  policy service service-set snmp\n",b"  policy service service-set http\n",\
                    b"  policy service service-set https\n",b"  policy service service-set ftp\n",\
                    b"  policy service service-set donghuan2\n",b"  policy service service-set donghuan3\n",\
                    b"  policy source address-set vpcserver\n",b"  policy source address-set natgateway\n",\
                    b"  policy destination address-set networks\n",b"#\n",b" policy 3\n",\
                    b" description for backhaul data requested by spacex\n",b"  action permit\n",\
                    b"  policy service service-set pertcp\n",b"  policy source address-set vpcserver\n",\
                    b"  policy source address-set bingqi\n",b"  policy source address-set natgateway\n",\
                    b"  policy destination address-set networks\n",b"#\n",b" policy 4\n",\
                    b" description for remoteaccess\n",b"  action permit\n",b"  policy service service-set telnet\n",\
                    b"  policy service service-set ssh\n",b"  policy source address-set network1\n",\
                    b"  policy source address-set vpcserver\n",b"  policy destination address-set networks\n",b"#\n",\
                    b"policy interzone trust untrust outbound\n",b" policy 1\n",\
                    b" description for detecting connectivity\n",b"  action permit\n",\
                    b"  policy service service-set icmp\n",b"#\n",b" policy 2\n",\
                    b" description for mangement outflow\n",b"  action permit\n",b"  policy service service-set ntp\n",\
                    b"  policy service service-set snmptrap\n",b"  policy service service-set syslog\n",\
                    b"  policy service service-set tftp\n",b"  policy service service-set radius\n",\
                    b"  policy service service-set donghuan1\n",b"  policy source address-set networks\n",\
                    b"  policy destination address-set vpcserver\n",b"#\n",b"  firewall defend http-flood enable\n",\
                    b"  firewall defend port-scan enable\n",b"  firewall defend ip-sweep enable\n",\
                    b"  firewall defend teardrop enable\n",b"  firewall defend ip-fragment enable\n",\
                    b"  firewall defend tcp-flag enable\n",b"  firewall defend fraggle enable\n",\
                    b"  firewall defend icmp-redirect enable\n",b"  firewall defend large-icmp enable\n",\
                    b"  firewall defend ping-of-death enable\n",b"  firewall defend icmp-flood enable\n",\
                    b"  firewall defend udp-flood enable\n",b"  firewall defend udp-flood zone dmz max-rate 1000\n",\
                    b"  firewall defend syn-flood enable\n",\
                    b"  firewall defend syn-flood zone dmz alert-rate 3000 max-rate 5000\n",\
                    b"  firewall defend syn-flood zone untrust alert-rate 3000 max-rate 5000\n",\
                    b"  firewall defend land enable\n",b"  firewall defend arp-flood enable\n",]

    dev_list_new = list_spilit(dev_list,n)
    print(dev_list_new)


    for sub_dev_list in dev_list_new:
        th = threading.Thread(target=fw_cfg_distribute, args=(sub_dev_list,command_list))
        threadpool.append(th)

    start = time.time()

    for th in threadpool:
        th.start()

    for th in threadpool:
        threading.Thread.join(th)

    end = time.time()
    print(end - start)
    with open('./result/result.txt', 'w', encoding='utf-8') as f:
        f.write(str(result_list))

if __name__ == '__main__':
    main()