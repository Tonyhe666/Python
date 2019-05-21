# !/usr/bin/python
# _*_ coding:utf-8 _*_

import os
import plistlib

def walkFile(rootdir):
    dict1 = {}
    dict2 = {}
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in dirnames:  # 输出文件夹信息
        #     # print("parent is:" + parent)
        #     # print("dirname is:" + dirname)
        #     # print("the full name of the file is:" + os.path.join(parent, dirname))  # 输出文件夹路径信息
        #     print(os.path.join(parent, dirname))  # 输出文件夹路径信息

        for filename in filenames:  # 输出文件信息
            # print("parent is:" + parent)
            # print("filename is:" + filename)
            # print("the full name of the file is:" + os.path.join(parent, filename))  # 输出文件路径信息
            # print(os.path.join(parent, filename))  # 输出文件路径信息
            if dict1.has_key(filename):
                print(dict1[filename])
                print(os.path.join(parent, filename))  # 输出文件路径信息
                dict2[filename] = os.path.join(parent, filename)
            else:
                dict1[filename] = os.path.join(parent, filename)


def walkFileCCB(rootdir):
    dict1 = {}
    dict2 = {}
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            if os.path.splitext(filename)[-1] == ".ccb":
                plistlib.readPlist(os.path.join(parent, filename))
            if dict1.has_key(filename):
                print(dict1[filename])
                print(os.path.join(parent, filename))  # 输出文件路径信息
                dict2[filename] = os.path.join(parent, filename)
            else:
                dict1[filename] = os.path.join(parent, filename)

if __name__ == '__main__':
    walkFile("/Users/heliang/rafotech/GuiYangCompanyClient/mahjong/res/img/")

    #plist = plistlib.readPlist("/Users/heliang/rafotech/GuiYangCompanyClient/GuiYangArtResource/GuiYangChessUI/Resources/ccbi/ClubZhanji.ccb")
    #print(plist)