# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
#import psutil

nameList = []
processList = []
argList = []


def is_running(process_name):
    str = r'wmic process where name="'+process_name+r'" get processid'  #查询这个名字的pid
    f=os.popen(str)
    A=f.read()  ##
    if A.find('Pro')==-1:
        f.close()
        return False
    else:
        f.close()
        return True
    # return (bool)([1 if psutil.Process(pid).name() == process_name or psutil.Process(pid).name().split('.')[
    #     0] == process_name else 0 for pid in psutil.pids()].count(1))


def create_file(file_path):
    f = open(file_path, 'w')
    f.close()


def main():
    # 判断是否存在配置文件
    if not os.path.exists('config.ini'):
        print('没有发现配置文件，创建配置文件ing')
        create_file('config.ini')
    else:
        with open(r'config.ini', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                lineArr = line.split(',')
                nameList.append(lineArr[0])
                processList.append(lineArr[1])
                argList.append(lineArr[2]) if len(lineArr) == 3 else argList.append('')
        # 读取配置文件到3个list

    if not os.path.exists('log.txt'):
        print('没有发现日志文件，创建日志文件ing')
        create_file('log.txt')

    while True:
        for key, name in enumerate(nameList):  # 期待运行的进程
            if not is_running(name):
                os.popen(processList[key] + ' ' + argList[key])
                with open(r'log.txt', 'a+', encoding='utf-8') as f:
                    f.write(str(datetime.now()) + ' 进程 %s 未启动，正在强制启动\n' % name)
        time.sleep(1)


if __name__ == '__main__':
    main()
