import logging


class Log:
    setHandler = False
    verbose = 1
    logfile = None
    streamhandler = None
    filehandler = None

    @staticmethod
    def increase_verbosity():
        global verbose
        if(Log.verbose < 5):
            Log.verbose = Log.verbose + 1
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
        lvl = (60 - (10 * Log.verbose))
        logging.root.handlers = []
        logging.basicConfig(level=lvl,
                            format="%(levelname)s: %(message)s")

        logging.shutdown()

    @staticmethod
    def fileoutput():
        lvl = (60 - (10 * Log.verbose))
        fileLogger = 0
        logging.basicConfig(level=lvl,
                            filemode='a',
                            format="%(asctime)s - %(levelname)s: %(message)s)"
                            )
        if not Log.logfile:
            Log.warning('Logfile is not set but nessesary.')
            return
        fileHandler = logging.FileHandler(Log.logfile)

        fileLogger = logging.getLogger()
        fileLogger.addHandler(fileHandler)
        fileLogger.setLevel(lvl)
        logging.shutdown()

    @staticmethod
    def handlerActivation(setHandler):
        Log.streamoutput()
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
