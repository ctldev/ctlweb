#!/usr/bin/env python3
from .database import Database
import sqlite3

class User(Database):
    """ An registered user
    """

    def __init__(self, name, pubkey):
        super().__init__()
        self.c_id = name
        self.c_pubkey = pubkey

    @classmethod
    def create(cls, attr):
        """ Creates User class out of an dict containing the following keys:
            * c_id
            * c_pubkey
        """
        return cls(attr['c_id'],attr['c_pubkey'])
