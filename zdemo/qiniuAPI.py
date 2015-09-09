#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os



from sevencow import CowException
from sevencow import Cow

allFileNum = 0
dirNameList=[]

ACCESS_KEY = 'xK4E9mgG3E4aDno7CAXemLMMrns6laJL5AAicJ_O'
SECRET_KEY = 'fsf2oCnVWJPtWZzkr1mou7gAXOSgyCZd6icSGwwk'
BUCKET_NAME = 'wish'

cow = Cow(ACCESS_KEY, SECRET_KEY)
b = cow.get_bucket(BUCKET_NAME)



def printPath(level, path):
    global allFileNum

    '''''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    list = []

    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        # print  path+'/'+fl
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1
        dirNameList.append(path+'/'+fl)

    return dirNameList


if __name__ == '__main__':
    #获得输入
    # file_path = sys.argv[1]

    photosList=[]
    list = printPath(3, '/home/ubuntu/Public/108385001')
    for rownum in range (0,len(list)):
        if list[rownum].endswith('.jpg') or  list[rownum].endswith('.png') :
            photosList.append(list[rownum])
    for rownmu in range (0,len(photosList)):
        # print photosList[rownmu]
        file_path = photosList[rownmu]
        print file_path
        #判断路径是否存在，是否是文件
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                d= b.put(file_path)
                print d['key'].decode("gbk").encode("utf-8")
            except CowException as e:
                print e.url,e.status_code,e.reason,e.content