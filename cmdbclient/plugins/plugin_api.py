#coding:utf8
from plugins.linux import sysinfo

def LinuxSysInfo():
    return  sysinfo.collect()


def WindowsSysInfo():
    '''
    只有是windows的时候才导入
    :return:
    '''
    from windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()
