#!/usr/bin/env python3
from .database import Database
from database.database import NoSuchTable
import sqlite3
from util import Log

class Component(Database):
    """ Is an component in the CTL-Database
    """
    def __init__(self, name, exe):
        """ Should not be used, use Component.create() instead.
        """
        super().__init__()
        self.c_id = name
        self.c_exe = exe

    @classmethod
    def create(cls, attr):
        """ attr is expected to be an dict with the following keys:
            * c_id: Componentname
            * c_exe: Path where the executable can be found
        """
        return cls(attr["c_id"], attr["c_exe"])

    def remove(self):
        """ Remove component with given name.
        
        Returns True if the component successfully removed.
        """
        Log.debug("Component.remove(): removing")
        super().remove()
        import os
        try:
            os.remove( os.path.join(Database.store, "%s.tgz" % self.c_id) )
        except IOError:
            Log.error("Component.remove(): unable to remove component file.")
            return False
        return True

    def upload_to_web(url):
        """ Upload the component to the given url

        """
        Log.debug("Uploading component to url %s" % url)
        import requests
        from os import path
        manifest_file = path.join(Database.store, "%s.tgz" % self.c_id)
        files = {'manifest': open(manifest_file, "rb")}
        r = requests.post(url, files=files)
        if r.status_code != requests.codes.ok:
            Log.critical("Error %s occured while upload" % r.status_code)


    @classmethod
    def add(cls, component):
        """ A given package will be added to the local database.

        A package has to be in the ctlweb-format which can be found in our
        docmuentation.

        returns newly created object
        """
        from os import path
        Log.debug("add(package): adding package to local database")
        # Create Database entry
        data = Component._unpack(component)
        comp = cls.create(data)
        try:
            comp.save()
        except NoSuchTable:
            comp.create_table().save()
        # Copy package to store
        import shutil
        try:
            target_name = path.join(Database.store, "%s.tgz" % data["c_id"])
            shutil.copy(component, target_name)
        except IOError:
            Log.critical("Unable to save component to Manifest store in %s" \
                    % store)
            exit(1)
        return comp

    @staticmethod
    def _unpack(component):
        """ Extracts important data out of the package. They are returned as a
        dictionary that works on Compontent.create().
        """
        import tarfile
        import os
        from datetime import datetime
        control_path = '/tmp/ctlcontrol-%s' % datetime.now().strftime('%s')
        control_file = control_path + "/control"
        with tarfile.open(component, 'r:gz') as comp:
            comp.extract("control", control_path, set_attrs = False)
        data = Component._read_control(control_file)
        os.remove(control_file)
        os.rmdir(control_path)
        return data

    @staticmethod
    def _read_control(control):
        """ Reads for the backend required keys of the control file. See
        Component.create() for more detail.
        """
        Log.debug("_read_control(): parsing control file %s")
        import configparser
        parser = configparser.ConfigParser()
        parser.read(control)
        try:
            name = parser['DEFAULT']['name']
        except KeyError:
            Log.critical("Found no component name")
            raise
        try:
            exe = parser['DEFAULT']['exe']
        except KeyError:
            Log.critical("Found no corresponding exe in component")
            raise
        return {"c_id": name, 
                "c_exe": exe,
                }

