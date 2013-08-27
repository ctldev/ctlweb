from .log import Log
from database import Database
import argparse
from database.pubkey import Pubkey

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--config', '-c', help='Own config file to be used')
parent_parser.add_argument('--verbose', '-v', default=1, action='count',
                           help='Increase output level')


def commit_settings(args):
    """ Sets the verbosity level & if nessesary it sets the user selected
    config file.
    """
    from os import path
    Log.set_verbosity(args.verbose)
    if args.config:
        Database(args.config)
    else:
        Database()
