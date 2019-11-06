# -*- coding: utf-8 -*-
import os
import psutil
from datetime import datetime
import time


def checkprocess():
    '''
    获取全部进程
    :return: list  of str
    '''
    p = []
    pid = psutil.pids()
    for i in pid:
        try:
            p.append(psutil.Process(i))
        except:
            pass
    return [i.name() for i in p]  # ！！！ except psutil.NoSuchProcess   迷


def main():
    processlist = []
    namelist = []
    arglist = []
    guardlist = []
    # 判断是否存在配置文件
    if 'config.ini' not in os.listdir('.'):
        print('没有发现配置文件，创建配置文件ing')
        f = open(r'config.ini', 'w')
        f.close()
    if 'log.txt' not in os.listdir('.'):
        print('没有发现日志文件，创建日志文件ing')
        f = open(r'log.txt', 'w')
        f.close()
    with open(r'config.ini', 'r') as f:
        for line in f.readlines():
            guardlist.append(line.strip())  # 每一行
    # 读取配置文件到3个list
    for line in guardlist:  # ！！！！！！
        if len(line.split(',')) == 2:
            name = line.split(',')[0]
            process = line.split(',')[1]
            args = ''
        elif len(line.split(',')) == 3:
            name = line.split(',')[0]
            process = line.split(',')[1]
            args = line.split(',')[2]
        else:
            raise ValueError('配置文件不正确')
        namelist.append(name)  # 守护进程名字
        processlist.append(process)  # 进程目录
        arglist.append(args)  # 参数

    # 当前运行进程的名字 list
    current_runing_process = checkprocess()
    while True:
        for key, name in enumerate(namelist):  # 期待运行的进程
            if (name not in current_runing_process) and (name not in [i.split('.')[0] for i in current_runing_process]):
                os.popen(processlist[key] + ' ' + arglist[key])
                with open(r'log.txt', 'a+', encoding='utf-8') as f:
                    f.write(str(datetime.now()) + ' 进程 %s 未启动，正在强制启动\n' % name)
                #current_runing_process = checkprocess()
        time.sleep(1)


if __name__ == '__main__':
    main()
