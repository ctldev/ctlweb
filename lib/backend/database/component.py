#!/usr/bin/env python3
from .database import Database
import sqlite3

class Component(Database):
    """ Is an component in the CTL-Database
    """
    def __init__(self, name, exe, manifest):
        """ Documentation text is not supported, because it could be to big.
        """
        super().__init__()
        self.c_id = name
        self.c_exe = exe
        self.c_manifest = manifest

    @classmethod
    def create(cls, attr):
        """ attr is expected to be an dict with the following keys:
            * c_id
            * c_exe
            * c_ci
        """
        return cls(attr["c_id"], attr["c_exe"], attr["c_manifest"])
