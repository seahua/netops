#!/usr/bin/python
# coding:utf8

import os


def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

def changepwd(path):
    with open(str(path), 'r', encoding='utf-8') as f:
        readlines = f.readlines()
    with open(str(path)+'.new', 'w', encoding='utf-8') as f:
        for line in readlines:
            line = line.replace('jieca0*123', 'Huaq*123')
            f.write(line)


dir = dirlist("/Users/huaqiang/Dropbox/Script/AutoLogin/iTerm2", [])
for doc in dir:
    # print(doc)
    changepwd(doc)