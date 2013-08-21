import sys
import os
from os.path import dirname,abspath
from database import Database
from database import User
from database import Web
from .settings import DEFAULT_CONFIG
 
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
