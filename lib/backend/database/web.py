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
        web = cls(attr['c_id'])
        if 'f_Pubkey_pubkey' in attr and attr['f_Pubkey_pubkey']:
            web.add_key(attr['f_Pubkey_pubkey'])
        return web

    def _keyline(self):
        return 'command="bash -c ctl-register" {0}'
