#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
myFile = open('Table.txt', 'r')
allWords = []
line = myFile.readline()
while line:  
    getList = line.split('    ')
    for word in getList:
        if word[-1] == '\n':
            allWords.append(word[:-1])  # 去掉行末的'\n'
        else:  
            allWords.append(word) 
    line = myFile.readline()
myFile.close()

#去掉前两行
allvalue =allWords[2:len(allWords)]

# print allvalue[3].decode("gbk").encode("utf-8") 
# values = allWords[2].decode("gbk").encode("utf-8")

# print allvalue
#把一行通过 Tab分割
values=allvalue[0].split('\t')
print values