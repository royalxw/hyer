#coding:utf-8

from BeautifulSoup import BeautifulSoup
import re

R_TRIM=re.compile("<.*?>",re.M|re.S)

def regexp(str):
    """返回一个正则表达式"""
    return re.compile(str,re.M|re.S);

def list(str):
    """返回一个list,是原文以||分隔"""
    return str.split("||")

class NoneConfig(dict):
    """当没有查找到节点的时候返回的东西"""
    def value(self):
        return None
    def __getitem__(self,key):
        return NoneConfig()


class Config(dict):
    """
    话说一米六二同志特别懒,这个配置文件的解析,就是证明:
    这个配置文件解析类,居然就是用的BeautifulSoup来解析的,懒到家了....
    @brief
    Example:
    //file demo.conf
    <root>
        <db type="string>
            host=localhost;user=root;pass=;db=test;
        </db>
    </root>
    
    #file test.py
    import hyer.config
    config=hyer.config.Config(open("demo.conf").read())
    print config["root"]["db"].values()
    """
    def __init__(self,content,last_find=None):
        self.content=content
        self.last_find=last_find
        self.soup= BeautifulSoup(self.content)
        self.builders={
                "string":str,
                "regexp":regexp,
                "list":list,
                "python":eval
                }
    def __str__(self):
        return self.content

    def values(self):
        results=[]
        for item in self.last_find:
            try:
                type=item["type"]
            except:
                type="string"
            results.append(self.builders[type](R_TRIM.sub("",str(item))))
        return results

    def confstrings(self):
        results=[]
        for item in self.last_find:
           results.append(str(item))
        return results

    def __getitem__(self,key):
        data=self.soup.findAll(key)
        self.last_find=data
        if data==None:
            return NoneConfig()
        else:
            return Config(str(data),self.last_find)
