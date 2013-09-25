#!/usr/bin/env python3
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
        return 'command="bash -lc ctl-init" {0}'

    def save(self):
        """ Overrides new users with the same old name. """
        from .database import InstanceAlreadyExists
        try:
            super().save()
        except InstanceAlreadyExists as e:
            self.c_pk = e.original().c_pk
            super().save()
