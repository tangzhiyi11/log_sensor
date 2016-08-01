#!/usr/bin/env python
# coding=utf-8

#product log into file

import time

def main():
    f = open("write_log.txt",'w')
    num = 0
    while 1 :    
        num += 1
        logstr = str(num) + ' log for test!\n'
        f.write(logstr)
        print logstr.strip()
        f.flush()
        time.sleep(2)
        if num > 10000000:
            break
    f.close()

if __name__ == "__main__":
    main()
