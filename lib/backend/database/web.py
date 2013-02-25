#!/usr/bin/env python3
import sqlite3
from .database import Database

class Web(Database):
    """ An registerd ctlweb instance
    """

    def __init__(self, url, pubkey):
        super().__init__()
        self.c_id = url
        self.c_pubkey = pubkey

    @classmethod
    def create(cls, attr):
        """ attr is expected to be an dict with the following keys:
            * c_id
            * c_pubkey
        """
        return cls(attr['c_id'], attr['c_pubkey'])
