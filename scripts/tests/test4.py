def format_txt(file):
    context = ''
    with open(file) as f:
        readlines = f.readlines()
    with open(file, 'w') as f:
        for line in readlines:
            if ('DEVICE_NAME' in line) or ('DEVICE_SERIAL_NUMBER' in line) or ("can't connect to host" in line):
                context = context+(line)
        f.write(context)

def main():
    path = '/Users/huaqiang/Downloads/run_result.1/'
    file_name_list_txt = '/Users/huaqiang/Downloads/file_name.txt'
    file_name_list = []
    with open(file_name_list_txt) as f:
        for line in f:
            file_name_list.append(path+line.replace('\n', ''))

    for file in file_name_list:
        format_txt(file)


    log = []
    with open(file_name_list_txt) as f:
        for file_name in f:
            file_path = path + file_name.replace('\n', '')
            with open(file_path) as f1:
                readlines = f1.readlines()
                if len(readlines) == 1:
                    info = {
                        'host': file_name.replace('\n', ''),
                        'SN': "0",
                        'model': '0',
                        'conn': '0'
                            }
                else:
                    model = readlines[0].replace('DEVICE_NAME          : ', '').replace('\n', '').replace(' ', '')
                    sn = readlines[1].replace('DEVICE_SERIAL_NUMBER : ', '').replace('\n', '').replace(' ', '')
                    info = {
                        'host': file_name.replace('\n', '').replace(' ', ''),
                        'SN': sn,
                        'model': model,
                        'conn': '1'
                    }
                log.append(info)

    for item in log:
        print(item['host'].replace('.txt', ''), '\t', item['model'], '\t', item['SN'], '\t', item['conn'])





if __name__ == '__main__':
    main()
