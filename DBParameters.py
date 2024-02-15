# DBParameters.py
# Created by Burmese Coder on 2/13/24.

import yaml

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
class DBParameters:
    dict_ok = False
    
    def __init__(self, filename = None):
        if filename:
            self.filename = filename
            stream = open(filename, 'r')
            self.paramdict = yaml.load(stream, Loader = Loader)
            self.dict_ok = True
            
    def uri(self):
        if self.dict_ok:
            connect = self.paramdict["connectionparameters"]
            url = connect["connectprotocol"] + '://' + connect["username"]+ ':' + connect["password"] + '@' + connect["host"] + connect['port'] + '/' 
            webparams = connect["webparams"]
            if webparams:
                url += '?'
                curitem = 0
                for key, value in webparams.items():
                    curitem += 1
                    url += key + "=" + str(value).lower() 
                    if curitem < len(webparams):
                        url += "&" 

                
            return url
        
