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
 
if __name__ == '__main__':
     print main('wf.txt')