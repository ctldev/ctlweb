#!/usr/bin/env python3
import sqlite3
from .access import Access

class User(Access):
    """ An registered user
    """

    @classmethod
    def create(cls, attr):
        """ Creates User class out of an dict containing the following keys:
            * c_id
            * c_pubkey
        """
        return cls(attr['c_id'],attr['c_pubkey'])

    def _keyline():
        return 'command="bash -c ctl-init" %s' % c_pubkey
