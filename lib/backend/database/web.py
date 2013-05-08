#!/usr/bin/env python3
import sqlite3
from .access import Access

class Web(Access):
    """ An registerd ctlweb instance
    """

    @classmethod
    def create(cls, attr):
        """ attr is expected to be an dict with the following keys:
            * c_id
            * c_pubkey
        """
        return cls(attr['c_id'], attr['c_pubkey'])

    def _keyline():
        return 'command="bash -c ctl-register" %s' % c_pubkey
