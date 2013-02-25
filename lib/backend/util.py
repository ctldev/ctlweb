import logging
import sys
import os


class Log:
    setHandler = False
    verbose = 0
    
    @staticmethod   
    def increase_verbosity(verbose):
        if(verbose < 5):    
            verbose = verbose + 1
        Log.setHandler = Log.handlerActivation(Log.setHandler) 
        return verbose
    
    @staticmethod    
    def choose_level(verbose):
        if verbose == 1:
            return 50 
        elif verbose == 2:
            return 40
        elif verbose == 3:
            return 30
        elif verbose == 4:
            return 20
        elif verbose == 5:
            return 10
        else: 
            return 60
    
    @staticmethod
    def streamoutput(lvl):
        root = 0
        root = logging.getLogger()
        logging.root.handlers=[] 
        logging.basicConfig(level = lvl,
                            format = "%(levelname)s: %(message)s")

        logging.shutdown()

    @staticmethod
    def fileoutput(lvl):
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
        Log.streamoutput(Log.choose_level(Log.verbose + 1))
        Log.fileoutput(Log.choose_level(Log.verbose + 1))
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
   
