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
            * f_Pubkey_pubkey
        """
        user = cls(attr['c_id'])
        if 'f_Pubkey_pubkey' in attr and attr['f_Pubkey_pubkey']:
            user.add_key(attr['f_Pubkey_pubkey'])
        return user

    def _keyline(self):
        return 'command="bash -c ctl-init" {0}'
