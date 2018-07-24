import os
import re


def eachFile(filepath):
    file_list = []
    file_dir = os.listdir(filepath)
    # print(file_dir)
    for file in file_dir:
        file_url = os.path.join('%s%s' % (filepath, file))
        file_list.append(file_url)
    return file_list


def replace_profile(file_url, password):
    all_lines = []
    with open(file_url, 'r') as f:
        all_lines = f.readlines()
    f.close()

    with open(file_url, 'w') as f:
        for line in all_lines:
            line = re.sub(r'qiang.hua',r'yan.shao',line)
            line = re.sub(r'jieca0\*123',password,line)
            f.writelines(line)
    f.close()


def main():
    password = input('password: ')
    for i in range(0, 100):
       print('\n')

    file_dir = '/Users/huaqiang/Dropbox/Script/AutoLogin/iTerm2_copy/'
    file_list = eachFile(file_dir)
    for file in file_list:
        replace_profile(file, password)


if __name__ == '__main__':
    main()