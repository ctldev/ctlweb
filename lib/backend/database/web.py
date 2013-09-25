#!/usr/bin/env python3
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
        return 'command="bash -lc ctl-webinit" {0}'

    def save(self):
        from .database import InstanceAlreadyExists
        try:
            super().save()
        except InstanceAlreadyExists as e:
            self.c_pk = e.original().c_pk
            super().save()
