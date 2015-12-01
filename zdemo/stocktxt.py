#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
myfile = open('Table.txt', 'r')  
allWords = []  
line = myfile.readline()  
while line:  
    list = line.split('    ')  
    for word in list:  
        if word[-1]=='\n':  
            allWords.append(word[:-1])  #去掉行末的'\n'  
        else:  
            allWords.append(word) 
    line = myfile.readline()  
myfile.close()    

print allWords[0].decode("gbk").encode("utf-8") + allWords[1].decode("gbk").encode("utf-8")
#print allWords[0] + allWords[1]
# print allWords[2].decode("gbk").encode("utf-8")
# print allWords[3].decode("gbk").encode("utf-8")
# print allWords[4].decode("gbk").encode("utf-8")
