# coding:utf-8
from core import info_collection
from core import api_token
from conf import settings
# import urllib2
import urllib,sys,os,json,datetime,requests



class ArgvHandler(object):
    def __init__(self,argv_list):
        self.argvs = argv_list
        self.parse_argv()


    def parse_argv(self):
        '''
        解析参数
        :return:
        '''
        if len(self.argvs) >1:
            if hasattr(self,self.argvs[1]):
                func = getattr(self,self.argvs[1])
                func()
            else:
                self.help_msg()
        else:
            self.help_msg()


    def help_msg(self):
        # 打印帮助信息
        msg = '''
        collect_data
        run_forever
        get_asset_id
        report_asset
        '''
        print(msg)


    def collect_data(self):
        '''收集信息'''
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()
        print(asset_data)


    def run_forever(self):
        '''当做一个进程执行,这里留空'''
        pass


    def __attach_token(self,url_str):
        '''generate md5 by token_id and username,and attach it on the url request'''

        user = settings.Params['auth']['user']
        token_id = settings.Params['auth']['token']

        md5_token,timestamp = api_token.get_token(user,token_id)
        url_arg_str = "user=%s&timestamp=%s&token=%s" %(user,timestamp,md5_token)
        #print(url_arg_str)
        if "?" in url_str:#already has arg
            new_url = url_str + "&" + url_arg_str
        else:
            new_url = url_str + "?" + url_arg_str
        return  new_url


    def __submit_data(self,action_type,data,method):
        '''
        不同的url,和资产数据传给__submit__data处理得到服务器返回的信息
        '''
        if action_type in settings.Params['urls']:
            if type(settings.Params['port']) is int:
                url = "http://%s:%s%s" %(settings.Params['server'],settings.Params['port'],settings.Params['urls'][action_type])
            else:
                url = "http://%s%s" %(settings.Params['server'],settings.Params['urls'][action_type])

            url =  self.__attach_token(url)
            print('Connecting [%s], it may take a minute' % url)

            if method == "get":
                args = ""
                for k,v in data.items():
                    args += "&%s=%s" %(k,v)
                args = args[1:]
                url_with_args = "%s?%s" %(url,args)
                try:
                    req = urllib.request.Request(url_with_args)
                    req_data = urllib.request.urlopen(req,timeout=settings.Params['request_timeout'])
                    callback = req_data.read()
                    print("-->server response:",callback)
                    return callback
                except urllib.request.URLError as e:
                    sys.exit("\033[31;1m%s\033[0m" % e)

            elif method == "post":
                try:
                    data_encode = urllib.parse.urlencode(data).encode()
                    req = urllib.request.Request(url=url,data=data_encode)
                    res_data = urllib.request.urlopen(req,timeout=settings.Params['request_timeout'])
                    callback = res_data.read()
                    callback = json.loads(callback.decode())
                    print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" %(method,url,callback))
                    return callback

                    # res = requests.post(url=url,data=data)
                    # data = res.content
                    # a = data.decode()
                    # callback = json.loads(a)
                    # print("\033[31m[%s]:[%s]\033[0m response:\n%s" %(method,url,callback))
                    # return callback
                except Exception as e:
                    print("是这里的问题")
                    sys.exit("\033[31;1m%s\033[0m" % e)
        else:
            print("上传的url不存在！")
            raise KeyError



    def load_asset_id(self,sn=None):
        '''加载资产id,如果是个新资产的话是获取不到资产id'''
        asset_id_file = settings.Params['asset_id']
        has_asset_id = False
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read().strip()
            if asset_id.isdigit():
                return  asset_id
            else:
                has_asset_id =  False
                # print("asset_id is none")
        else:
            has_asset_id =  False


    def __update_asset_id(self,new_asset_id):
        '''
        服务器获取到了资产id,写入到文件保存
        :param new_asset_id:
        :return:
        '''
        asset_id_file = settings.Params['asset_id']
        f = open(asset_id_file,"w")
        f.write(str(new_asset_id))
        f.close()


    def report_asset(self):
        '''
        搜集数据并汇报
        '''

        # 实例化一个搜集信息实例
        obj = info_collection.InfoCollection()
        # 通过collect()搜集信息
        asset_data = obj.collect()
        # 获取资产id
        asset_id = self.load_asset_id(asset_data["sn"])
        if asset_id: # 如果获取到资产id,资产数据中添加上资产id,并设置上传url
            asset_data["asset_id"] = asset_id
            post_url = "asset_report"

        else:
            '''
            会汇报到另外一个url,将这条资产信息添加到待批准区,批准后会返回资产id
            '''

            asset_data["asset_id"] = None
            post_url = "asset_report_with_no_id"

        # 将搜集的资产数据序列化下,传给__submit__data
        data = {"asset_data": json.dumps(asset_data)}
        # 不同的url,和资产数据传给__submit__data处理得到服务器返回的信息
        response = self.__submit_data(post_url,data,method="post")
        if "asset_id" in response:
            self.__update_asset_id(response["asset_id"])
        # 写入日志
        self.log_record(response)


    def log_record(self,log,action_type=None):
        with open(settings.Params['log_file'],"a") as f:
            if log is str:
                pass
            if type(log) is dict:

                if "info" in log:
                    for msg in log["info"]:
                        log_format = "%s\tINFO\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                        #print(msg)
                        f.write(log_format)
                if "error" in log:
                    for msg in log["error"]:
                        log_format = "%s\tERROR\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                        f.write(log_format)
                if "warning" in log:
                    for msg in log["warning"]:
                        log_format = "%s\tWARNING\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                        f.write(log_format)

            f.close()



    #def __get_asset_id_by_sn(self,sn):
    #    return  self.__submit_data("get_asset_id_by_sn",{"sn":sn},"get")
