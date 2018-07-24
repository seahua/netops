from scripts.modules.network import NetworkMgmt


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


def main():
    result = []
    icc_result = []
    input_file = './4g.txt'
    host_list = get_host(input_file)
    for host in host_list:
        result.append(get_context(host))

    for i in result:
        if i['result'] == 0:
            iccid = 0
            print(i['host'], '\t', iccid)
        else:
            iccid = get_iccid(i['screen_buffer'])
            print(i['host'], '\t', iccid)


if __name__ == '__main__':
    main()
