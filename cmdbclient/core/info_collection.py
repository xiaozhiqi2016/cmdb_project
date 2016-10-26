#coding:utf8
from plugins import plugin_api
import json,platform,sys


class InfoCollection(object):
    def __init__(self):
        pass


    def get_platform(self):
        '''
        获取系统
        '''
        os_platform = platform.system()

        return os_platform


    def collect(self):
        '''
        执行相应系统的执行方法
        不同系统执行不同的方法搜集资产信息
        '''
        os_platform = self.get_platform()
        try:
            func = getattr(self,os_platform)
            info_data = func()
            formatted_data = self.build_report_data(info_data)
            return formatted_data
        except AttributeError as e:
            sys.exit("Error:CMDB doens't support os [%s]! " % os_platform)


    def Linux(self):
        sys_info = plugin_api.LinuxSysInfo()

        return sys_info


    def Windows(self):
        sys_info = plugin_api.WindowsSysInfo()
        print(sys_info)
        #f = file('data_tmp.txt','wb')
        #f.write(json.dumps(sys_info))
        #f.close()
        return sys_info


    def build_report_data(self,data):
        '''
        add token info in here before send
        '''

        return data
