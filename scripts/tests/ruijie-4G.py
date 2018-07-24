import threading
import time
import xlrd
import xlsxwriter

def get_dev_list(path):
    """根据简道云导出的输入文件input.xlsx备份交换机信息"""
    dev_list = []
    input_data = xlrd.open_workbook(path)  # '/Users/huaqiang/Downloads/input.xlsx')
    table = input_data.sheets()[0]
    row_count = table.nrows
    col_count = table.ncols
    for index in range(0, col_count):
        # print(table.row_values(0)[index])
        if table.row_values(0)[index].encode() == 'site_name'.encode():
            site_name_num = index
        if table.row_values(0)[index].encode() == 'vlan'.encode():
            vlan_num = index
        if table.row_values(0)[index].encode() == 'site_code'.encode():
            site_code_num = index
        if table.row_values(0)[index].encode() == 'svi_ip'.encode():
            svi_ip_num = index
        if table.row_values(0)[index].encode() == 'wan_ip'.encode():
            wan_ip_num = index
        if table.row_values(0)[index].encode() == 'lan_ip'.encode():
            lan_ip_num = index
        if table.row_values(0)[index].encode() == 'rev_ip'.encode():
            rev_ip_num = index
        if table.row_values(0)[index].encode() == 'loopback'.encode():
            loopback_num = index
        if table.row_values(0)[index].encode() == 'vlan101_ip'.encode():
            vlan101_ip_num = index
        if table.row_values(0)[index].encode() == 'conn_ip'.encode():
            conn_ip_num = index
        if table.row_values(0)[index].encode() == 'ospf_id'.encode():
            ospf_id_num = index
        if table.row_values(0)[index].encode() == 'area_id'.encode():
            area_id_num = index
        if table.row_values(0)[index].encode() == 'fw_brand'.encode():
            fw_brand_num = index
    # print(site_name_num,lan_ip_num)
    for index in range(1, row_count):
        dev_info = {
            'site_name': table.row_values(index)[site_name_num],
            'vlan': table.row_values(index)[vlan_num],
            'site_code': table.row_values(index)[site_code_num],
            'svi_ip': table.row_values(index)[svi_ip_num],
            'wan_ip': table.row_values(index)[wan_ip_num],
            'lan_ip': table.row_values(index)[lan_ip_num],
            'rev_ip': table.row_values(index)[rev_ip_num],
            'loopback': table.row_values(index)[loopback_num],
            'vlan101_ip': table.row_values(index)[vlan101_ip_num],
            'conn_ip': table.row_values(index)[conn_ip_num],
            'ospf_id': table.row_values(index)[ospf_id_num],
            'area_id': table.row_values(index)[area_id_num],
            'fw_brand': table.row_values(index)[fw_brand_num]
        }
        dev_list.append(dev_info)
    return dev_list

def huawei_config(device_info):
    site_name = device_info['site_name']
    vlan = device_info['vlan']
    site_code = device_info['site_code']
    svi_ip = device_info['svi_ip']
    wan_ip = device_info['wan_ip']
    lan_ip = device_info['lan_ip']
    rev_ip = device_info['rev_ip']
    loopback = device_info['loopback']
    vlan101_ip = device_info['vlan101_ip']
    conn_ip = device_info['conn_ip']
    ospf_id = device_info['ospf_id']
    area_id = device_info['area_id']
    fw_brand = device_info['fw_brand']

    huawei_template = [
        'interface Ethernet2/0/0',
        ' ospf network-type p2p',
        'interface Ethernet0/0/0',
        ' undo dhcp client enable',
        ' speed 100',
        ' duplex full',
        ' alias WAN0',
        ' ip address ' + conn_ip + ' 30',
        'ip address-set wireless type object',
        ' address 1 172.18.0.0 mask 255.255.0.0 description for 4G-conn',
        'policy interzone local untrust outbound',
        ' policy 3',
        ' description for 4g-mgmt',
        '  action permit',
        '  policy service service-set telnet',
        '  policy service service-set ssh',
        '  policy destination address-set wireless',
        'ospf ' + str(int(ospf_id)) + ' router-id ' + conn_ip,
        ' area ' + str(int(area_id)),
        '  network ' + lan_ip + ' 0.0.0.0',
        '  network ' + wan_ip + ' 0.0.0.0',
        'ip route-static 172.19.249.60 255.255.255.252 ' + vlan101_ip,
        'undo ip route-static 0.0.0.0 0.0.0.0 ' + svi_ip,
    ]

    return huawei_template


def h3c_config(device_info):
    site_name = device_info['site_name']
    vlan = device_info['vlan']
    site_code = device_info['site_code']
    svi_ip = device_info['svi_ip']
    wan_ip = device_info['wan_ip']
    lan_ip = device_info['lan_ip']
    rev_ip = device_info['rev_ip']
    loopback = device_info['loopback']
    vlan101_ip = device_info['vlan101_ip']
    conn_ip = device_info['conn_ip']
    ospf_id = device_info['ospf_id']
    area_id = device_info['area_id']
    fw_brand = device_info['fw_brand']

    h3c_template = [
        'interface Eth0/0',
        ' ip address ' + conn_ip + ' 30',
        'interface Eth0/1',
        ' ospf network-type p2p',
        'ospf ' + str(int(ospf_id)) + ' router-id ' + conn_ip,
        ' area ' + str(int(area_id)),
        '  network ' + lan_ip + ' 0.0.0.0',
        '  network ' + wan_ip + ' 0.0.0.0',
        'ip route-static 172.19.249.60 255.255.255.252 ' + vlan101_ip,
        'undo ip route-static 0.0.0.0 0.0.0.0 ' + svi_ip
    ]

    return h3c_template


def sw_config(device_info):
    site_name = device_info['site_name']
    vlan = device_info['vlan']
    site_code = device_info['site_code']
    svi_ip = device_info['svi_ip']
    wan_ip = device_info['wan_ip']
    lan_ip = device_info['lan_ip']
    rev_ip = device_info['rev_ip']
    loopback = device_info['loopback']
    vlan101_ip = device_info['vlan101_ip']
    conn_ip = device_info['conn_ip']
    ospf_id = device_info['ospf_id']
    area_id = device_info['area_id']
    fw_brand = device_info['fw_brand']

    sw_template = [
        'interface vlan ' + str(int(vlan)),
        ' ospf network-type p2p',
        'ospf ' + str(int(ospf_id)),
        ' area ' + str(int(area_id)),
        '  network ' + svi_ip + ' 0.0.0.0',
        'undo ip route ' + lan_ip + ' 29 ' + wan_ip
    ]

    return sw_template


def main():
    dev_list = get_dev_list('/Users/huaqiang/Downloads/ruijie_4G_input.xlsx')

    for device_info in dev_list:
        if device_info['fw_brand'] == '华为':
            fw_config = huawei_config(device_info)
        if device_info['fw_brand'] == '华三':
            fw_config = h3c_config(device_info)

        sw_configuration = sw_config(device_info)

        with open('/Users/huaqiang/Dropbox/工作/千寻/项目/2018双路由-无线/山东、江苏/config/' + \
                          device_info['site_name'] + '_' + device_info['wan_ip'] +  '.txt', 'a', encoding='utf-8') as f:
            f.write('# FW:' + '\r\n')

            for line in fw_config:
                f.write(line + '\r\n')

            f.write('\r\n\r\n\r\n')
            f.write('# Switch' + '\r\n')

            for line in sw_configuration:
                f.write(line + '\r\n')


if __name__ == '__main__':
    main()