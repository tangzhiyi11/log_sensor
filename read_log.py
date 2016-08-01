#!/usr/bin/env python
# coding=utf-8

import threading
import time
import os
import Queue
import commands

#count file line nums
def read_linenum(file_path):
    command = 'wc -l ' + file_path
    status,output = commands.getstatusoutput(command)
    if status == 0:
        return output.split(' ')[0]
    else:
        return 0

#read logs from logfile
def read_log(file_path,data):
    f = open(file_path,'r')
    num = 0
    while True:
        current_lines = read_linenum(file_path)
        if num < int(current_lines):
            while num < int(current_lines):
                log = f.readline().strip()
                num += 1
                print "read log:{log}".format(log=log)
                data.put(log)
        time.sleep(5)
    f.close()

#write logs into local file
def write_log(result_path,result):
    while True:
        if result.empty():
            time.sleep(5)
        else:
            f = open(result_path,'a')
            while not result.empty():
                log = result.get()
                print 'write log from queue: %s' % log
                f.write(log+'\n')
            f.close()

#parse logs and put into result queue
def parse_log(data,result):
    while True:
        if data.empty():
            time.sleep(5)
        else:
            while not data.empty():
                log = data.get()
                print "put log into result queue: %s" % log
                result.put(log)

def main():
    data = Queue.Queue()
    result = Queue.Queue()
    file_path = "write_log.txt"
    result_path = "result_log.txt"
    threads = []
    t1 = threading.Thread(target=read_log,args=(file_path,data,))
    threads.append(t1)
    t2 = threading.Thread(target=parse_log,args=(data,result,))
    threads.append(t2)
    t3 = threading.Thread(target=write_log,args=(result_path,result,))
    threads.append(t3)
    
    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
