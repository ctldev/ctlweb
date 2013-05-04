import sys
import os
from os.path import dirname,abspath
from database import Database
from database import User
from database import Web
from settings import DEFAULT_CONFIG
 
def hash_file(file, block_size=512):
    import hashlib
    import base64
    md5 = hashlib.md5()
    with open(file,'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return base64.b64encode(md5.digest()).decode('utf8')

#determines the calling commando and returns the class accordingly 
def find_class():
    if(sys.argv[0] == "ctl-register"):
        return User
    elif(sys.argv[0] == "ctl-web"):
        return Web
        

def add(reg_id,reg_pubkey,database):
    cls = find_class()
    if(database == None):
        d = Database()
    else:
        d = Database(database)
    if(cls == "ctl-web"):
        add_instance = cls(reg_id, reg_pubkey)
        add_instance.save()
    elif(cls == "ctl-register"):
        add_instance = cls(reg_id, reg_pubkey)
        add_instance.save()

def remove(reg_id,reg_pubkey,database):
    cls = find_class() 
    if(database == None):
        d = Database()
    else:
        d = Database(database)
    if(cls == "ctl-web"):
        rm_instance = cls(reg_id, reg_pubkey)
        get_exacly(cls,reg_id).remove()
    elif(cls == "ctl-register"):
        rm_instance = cls(reg_id, reg_pubkey)
        get_exactly(cls,reg_id).remove()

def overview(time_since='all'):
    cls = find_class()
    print(get(cls,time_since))
