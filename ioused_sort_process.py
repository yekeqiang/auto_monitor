#!/usr/bin/env python 
#-*- coding:utf-8 -*- 
# 查询出使用 IO 排名前几的进程
# 使用方法：
# python io_sort_process.py  5 4 3
# 第一个参数的含义：每次收集读写数据的间隔秒数
# 第二个参数的含义：打印出读写最多的n个进程  
# 第三个参数的含义：脚本运行的次数
#
#
### END INIT INFO
import os
import re
import sys
import time
from string import strip
 
####
sys_proc_path = '/proc/'
re_find_process_number = '^\d+$'
 
####
# 通过/proc/$pid/io获取读写信息
####
def collect_info():
    _tmp = {}
    re_find_process_dir = re.compile(re_find_process_number)
    for i in os.listdir(sys_proc_path):
        if re_find_process_dir.search(i):
            # 获得进程名
            process_name = open("%s%s/stat" % (sys_proc_path, i), "rb").read().split(" ")[1]
            # 读取io信息
            rw_io = open("%s%s/io" % (sys_proc_path, i), "rb").readlines()
            for _info in rw_io:
                cut_info = strip(_info).split(':')
                if strip(cut_info[0]) == "read_bytes":
                    read_io = int(strip(cut_info[1]))
                if strip(cut_info[0]) == "write_bytes":
                    write_io = int(strip(cut_info[1]))
            _tmp[i] = {"name":process_name, "read_bytes":read_io, "write_bytes":write_io}
    return _tmp
 
 
def main(_sleep_time, _list_num):
    _sort_read_dict = {}
    _sort_write_dict = {}
    # 获取系统读写数据
    process_info_list_frist = collect_info()
    time.sleep(_sleep_time)
    process_info_list_second = collect_info()
    # 将读数据和写数据进行分组，写入两个字典中
    for loop in process_info_list_second.keys():
        second_read_v = process_info_list_second[loop]["read_bytes"]
        second_write_v = process_info_list_second[loop]["write_bytes"]
        try:
            frist_read_v = process_info_list_frist[loop]["read_bytes"]
        except:
            frist_read_v = 0
        try:
            frist_write_v = process_info_list_frist[loop]["write_bytes"]
        except:
            frist_write_v = 0
        # 计算第二次获得数据域第一次获得数据的差
        _sort_read_dict[loop] = second_read_v - frist_read_v
        _sort_write_dict[loop] = second_write_v - frist_write_v
    # 将读写数据进行排序
    sort_read_dict = sorted(_sort_read_dict.items(),key=lambda _sort_read_dict:_sort_read_dict[1],reverse=True)
    sort_write_dict = sorted(_sort_write_dict.items(),key=lambda _sort_write_dict:_sort_write_dict[1],reverse=True)
    # 打印统计结果
    print "pid     process     read(bytes) pid     process     write(btyes)"
    for _num in range(_list_num):
        read_pid = sort_read_dict[_num][0]
        write_pid = sort_write_dict[_num][0]
        res = "%s" % read_pid
        res += " " * (8 - len(read_pid)) + process_info_list_second[read_pid]["name"]
        res += " " * (12 - len(process_info_list_second[read_pid]["name"])) + "%s" % sort_read_dict[_num][1]
        res += " " * (12 - len("%s" % sort_read_dict[_num][1])) + write_pid
        res += " " * (8 - len(write_pid)) + process_info_list_second[write_pid]["name"]
        res += " " * (12 - len("%s" % process_info_list_second[write_pid]["name"])) + "%s" % sort_write_dict[_num][1]
        print res
    print "\n" * 1
 
 
if __name__ == '__main__':
    try:
        _sleep_time = sys.argv[1]
    except:
        _sleep_time = 3
    try:
        _num = sys.argv[2]
    except:
        _num = 3
    try:
        loop = sys.argv[3]
    except:
        loop = 1
    for i in range(int(loop)):
        main(int(_sleep_time), int(_num))