#!/usr/bin/env python3
from .database import Database
from database.database import NoSuchTable
import sqlite3
from util import Log


class Component(Database):

    """ Is an component in the CTL-Database
    """
    def __init__(self, name, exe, exe_hash):
        """ Should not be used, use Component.create() instead.
        """
        super().__init__()
        self.c_id = name
        self.c_exe = exe
        self.c_exe_hash = exe_hash

    @property
    def _component_file(self):
        import os
        return os.path.join(Database.store, "%s.tgz" % self.c_id)

    @classmethod
    def create(cls, attr):
        """ attr is expected to be an dict with the following keys:
            * c_id: Componentname
            * c_exe: Path where the executable can be found
        """
        return cls(attr["c_id"], attr["c_exe"], attr["c_exe_hash"])

    def remove(self):
        """ Remove component with given name.

        Returns True if the component successfully removed.
        """
        Log.debug("Component.remove(): removing")
        super().remove()
        import os
        try:
            os.remove(self._component_file)
        except IOError:
            Log.error("Component.remove(): unable to remove component file.")
            return False
        return True

    def upload_to_web(self, url):
        """ Upload the component to the given url

        """
        Log.debug("Uploading component to url %s" % url)
        import requests
        from os import path
        manifest_file = self._component_file
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
            target_name = comp._component_file
            shutil.copy(component, target_name)
        except IOError:
            Log.critical("Unable to save component to Manifest store in %s"
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
            comp.extract("control", control_path, set_attrs=False)
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
            exe_hash = parser['DEFAULT']['exe_hash']
        except KeyError:
            Log.critical("Found no corresponding exe in component")
            raise
        return {"c_id": name,
                "c_exe": exe,
                "c_exe_hash": exe_hash,
                }

    def execute(self, args=None):
        """ Executes the component with the given argument string
        """
        import subprocess
        import shlex
        import sys
        args = '%s %s' % (self.c_exe, args)
        args = shlex.split(args)
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print('Error occured while running ctl command.\nran: %s' %
                  ' '.join(args),
                  file=sys.stderr)
        except OSError:
            print('CTL Command not found, please contact the administrator.'
                  + '\nran: %s' % ' '.join(args),
                  file=sys.stderr)

    def save(self):
        """ """
        from .database import InstanceAlreadyExists
        try:
            super().save()
        except InstanceAlreadyExists as e:
            opponent = e.original()
            if self.c_exe_hash == opponent.c_exe_hash:
                self._merge(opponent)
            else:
                self._update(opponent)

    def _input(msg):
        return input(msg)

    def _merge(self, opponent):
        from util.build_component import merge_components
        import os
        Log.info('About to merge components.')
        merged_file = ""
        with open(self._component_file, 'r') as one:
            with open(opponent._component_file, 'r') as two:
                merged_file = merge_components(one, two)
        if not merged_file:
            Log.error('Was unable to merge components')
            return
        os.remove(self._component_file)
        os.rename(merged_file, self._component_file)

    def _update(self, opponent):
        while True:
            override = self._input('Shall I override the component %s? (y/N)' %
                                   self.c_id)
            override = override.strip().lower()
            if override[0] == 'n':
                Log.info('break!')
                return
            elif override[0] == 'y' or override[0] == 'j':
                Log.info('overriding.')
                self.c_pk = opponent.c_pk
                self.save()
                return
