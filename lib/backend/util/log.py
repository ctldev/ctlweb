import logging

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

