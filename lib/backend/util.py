import logging
import sys
import os


class Log:
    setHandler = False
    verbose = 0
    
    @staticmethod   
    def increase_verbosity():
        global verbose
        if(Log.verbose < 5):    
            Log.verbose = Log.verbose +  1
        Log.setHandler = Log.handlerActivation(Log.setHandler) 
    
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
        Log.streamoutput(60-(10*Log.verbose))
        Log.fileoutput(60-(10*Log.verbose))
        #verboselevel wird durch die Formel berechnet
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
   
