import logging
import sys
import os

DEFAULT_CONFIG = '/etc/ctlweb.conf'
""" Where the default config file comes from """

class Log:
    setHandler = False
    verbose = 1
    
    @staticmethod   
    def increase_verbosity():
        global verbose
        if(Log.verbose < 5):    
            Log.verbose = Log.verbose +  1
        Log.setHandler = Log.handlerActivation(Log.setHandler) 
    
    @staticmethod
    def set_verbosity(x):
        global verbose
        if (x <= 5):
            Log.verbose = x
        else:
            Log.verbose = 5
        Log.setHandler = Log.handlerActivation(Log.setHandler) 
    
    @staticmethod
    def streamoutput():
        lvl = (60-(10*Log.verbose))
        root = 0
        root = logging.getLogger()
        logging.root.handlers=[] 
        logging.basicConfig(level = lvl,
                            format = "%(levelname)s: %(message)s")

        logging.shutdown()

    @staticmethod
    def fileoutput():
        lvl = (60-(10*Log.verbose))
        fileLogger = 0
        logging.basicConfig(level = lvl,
                            filemode = 'a',
                            format = "%(asctime)s - %(levelname)s: %(message)s)"
                            )
        fileHandler = logging.FileHandler('ctl.log')
   
        fileLogger = logging.getLogger()
        fileLogger.addHandler(fileHandler)
        fileLogger.setLevel(lvl)
        logging.shutdown()

    @staticmethod 
    def handlerActivation(setHandler):
        Log.streamoutput()
        Log.fileoutput()
        return True
   
    @staticmethod 
    def debug(debugmsg):
        logging.debug(debugmsg)
   
    @staticmethod
    def info(infomsg):
        logging.info(infomsg)
   
    @staticmethod 
    def warning(warningmsg):
        logging.warning(warningmsg)
   
    @staticmethod 
    def error(errormsg):
        logging.error(errormsg)
   
    @staticmethod 
    def critical(criticalmsg):
        logging.critical(criticalmsg)
   
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

def add_component(component, config):
    """ Adds a component to the local system. Packages will be backuped in the
    Manifest_store directory """
    import tarfile
    import configparser
    import shutil
    from datetime import datetime
    from database.component import Component
    from database.database import NoSuchTable
    control_path = '/tmp/control-%s' % datetime.now().strftime('%s')
    control_file = control_path + "/control"
    with tarfile.open(component, 'r:gz') as comp:
        comp.extract("control", control_path, set_attrs = False)
    parser = configparser.ConfigParser()
    # Reading package file
    parser.read(control_file)
    Log.debug("add_component(): control file %s exists? %s" \
            % (control_file, os.path.isfile(control_file)) )
    Log.debug("add_component(): parsing control file.")
    try:
        name = parser['DEFAULT']['name']
    except KeyError:
        Log.critical("Found no component name")
        raise
    try:
        exe = parser['DEFAULT']['exe']
    except KeyError:
        Log.critical("Found no corresponding exe in component")
        raise
    try:
        ci = parser['DEFAULT']['ci']
    except KeyError:
        Log.critical("Found no corresponding ci in component")
        raise
    # switching to system config
    Log.debug("add_component(): parsing config file %s" % config)
    parser.read(config)
    os.remove(control_file)
    try:
        store = parser['Backend']['Manifest_store']
        Log.debug("add_component(): manifest store is %s" % store)
    except KeyError:
        Log.critical("No Manifest_store in config %s found" % config)
        raise
    c = Component(name, exe, ci)
    try:
        Log.debug("add_component(): saving compontent to %s%s.tgz" \
                % (store, name))
        shutil.copy(component, 
                "%s%s.tgz" % (store, name))
    except IOError:
        Log.critical("Unable to save component to Manifest store in %s" \
                % store)
        exit(1)
    try:
        c.save()
    except NoSuchTable:
        c.create_table()
        c.save()

#determines the calling commando and returns the class accordingly 
def find_class():
    if(sys.arg[0] == "ctl-register"):
        return User
    elif(sys.arg[0] == "ctl-web"):
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

    




