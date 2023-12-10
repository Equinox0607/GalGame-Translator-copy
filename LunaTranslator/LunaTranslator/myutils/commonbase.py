from myutils.utils import getproxy
from myutils.config import globalconfig,_TR,static_data
from myutils.wrapper import stripwrapper
from traceback import print_exc
import requests

class ArgsEmptyExc(Exception):
    def __init__(self,valuelist) -> None:
        super().__init__(' , '.join(valuelist)+_TR("不能为空"))

class proxysession(requests.Session):
    def __init__(self,_proxygetter) :
        super().__init__()
        self.proxygetter=_proxygetter
    def request(self,*args,**kwargs):
        kwargs['proxies']=self.proxygetter()
        return super().request(*args,**kwargs)
class commonbase:
    _globalconfig_key=None
    _setting_dict=None
    typename=None
    def langmap(self):
        return {}
    @property
    def proxy(self):
        if ('useproxy' not in  globalconfig[self._globalconfig_key][self.typename]) or globalconfig[self._globalconfig_key][self.typename]['useproxy']:
            return getproxy()
        else:
            return {'https':None,'http':None}
    @property
    def srclang(self):
        try:
            l=static_data["language_list_translator_inner"][globalconfig['srclang3']]
            return self.langmap_[l] 
        except:
            return ''
    @property
    def tgtlang(self):
        try:
            l=static_data["language_list_translator_inner"][globalconfig['tgtlang3']]
            return self.langmap_[l] 
        except:
            return ''
    @property
    def config(self):
        try:
            return stripwrapper(self._setting_dict[self.typename]['args'])
        except:
            return {}
    
    def countnum(self,query=None):
        if '次数统计' in self._setting_dict[self.typename]['args']:
            try: 
                self._setting_dict[self.typename]['args']['次数统计']=str(int(self.config['次数统计'])+1)
            except: 
                self._setting_dict[self.typename]['args']['次数统计']='1'
        if ('字数统计' in self._setting_dict[self.typename]['args'] ) and query:
            try: 
                self._setting_dict[self.typename]['args']['字数统计']=str(int(self.config['字数统计'])+len(query))
            except: 
                self._setting_dict[self.typename]['args']['字数统计']=str( len(query))
    def checkempty(self,items):
        emptys=[]
        for item in items:
            if (self.config[item])=='':
                emptys.append(item)
        if len(emptys):
            raise ArgsEmptyExc(emptys)
    @property
    def langmap_(self):
        _=dict(zip(static_data["language_list_translator_inner"],static_data["language_list_translator_inner"]))
        _.update({'cht':'zh'})
        _.update(self.langmap())
        return _
    def __init__(self,typename) -> None:
        self.typename=typename 
        self.session=proxysession(lambda:self.proxy)
        self.level2init()
    def level2init(self):
        pass