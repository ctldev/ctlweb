from .log import Log
from database import Database
import argparse

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--config', '-c', help='Own config file to be used')
parent_parser.add_argument('--verbose', '-v', default=1, action='count',
                           help='Increase output level')


def commit_settings(args):
    """ Sets the verbosity level & if nessesary it sets the user selected
    config file.
    """
    import configparser
    import sys
    from os import path
    if args is not None:
        Log.set_verbosity(args.verbose)
    if args is not None and args.config:
        Database(args.config)
    else:
        Database()
    cparser = configparser.ConfigParser()
    cparser.read(Database.config)
    try:
        dbg = cparser.get('Backend', 'debug')
        if dbg:
            Log.set_verbosity(5)
    except configparser.Error:
        Log.critical('Your Config-File seems to be malformed! Check your config'
                     ' file for the debug entry and try again.')
        sys.exit(1)
    try:
        file = cparser.get('Backend', 'logfile')
        file = path.expanduser(file)
        file = path.expandvars(file)
        file = path.abspath(file)
        Log.logfile = file
    except configparser.Error:
        Log.critical('Your Config-File seems to be malformed! Check your config'
                     ' file for the logfile entry and try again.')
        sys.exit(1)
