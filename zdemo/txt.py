#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import re
 
def main(filename):
    result = ''
    reader = open(filename, 'r')
    while True:
        line = reader.readline()
        if len(line) == 0:
            break
        if not line.startswith('		wf_'):
            continue
        pos = line.rfind('wf_')
        
        if pos < 0:
            continue
        result =result + '\r' +line[pos:]
    reader.close()
    return result


# myFile = open('Table.txt', 'r')
# allWords = []
# line = myFile.readline()
# while line:
#     getList = line.split('    ')
#     for word in getList:
#         if word[-1] == '\n':
#             allWords.append(word[:-1])  # 去掉行末的'\n'
#         else:
#             allWords.append(word)
#     line = myFile.readline()
# myFile.close()

if __name__ == '__main__':
     print main('wf.txt')