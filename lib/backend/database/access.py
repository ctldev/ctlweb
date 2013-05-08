from .database import Database

class Access(Database):
    """ All classes that provide ssh access modification are derived from this
    one.

    This class should not be used directly, it only provides special *add()*,
    *remove()* functions which are using the unimplemented *_keyline()*
    function.
    """
    authorized_keys_file = None

    def __init__(self, id, pubkey):
        super().__init__()
        self.c_id = id
        self.c_pubkey = pubkey

        import configparser
        from os import path
        reader = configparser.ConfigParser()
        reader.read(Database.config)
        if Access.authorized_keys_file: # Set authorized_keyfiles to grant access
            return
        try:
            Access.authorized_keys_file = reader['Backend','authorized_keys']
        except KeyError:
            home = path.expanduser('~')
            Access.authorized_keys_file = path.join( 
                    home, '.ssh', 'authorized_keys')
            

    def _keyline():
        """ Returns a authorized_keys compatible line with access definitions.
        """
        pass


    @classmethod
    def add(cls, attr):
        """ This method adds a new object to database and authorized_keys. 
        
        attr is expected to be a dictionary. 
        The attr are at least and have to be compatible with the create()
        attributes:
            * c_id
            * c_pubkey
        """
        # TODO add key to authorized_keys
        cls.create(attr)

    def remove(self):
        """ This method removes the object from database and authorized_keys.
        """
        # TODO remove key from authorized_keys
        super().remove()

    def _addkey(self):
        """ Adds the own access with the _keyline() to authorized_keys
        """
        with open(Access.authorized_keys_file, 'a') as authorized_key_file:
            authorized_key_file.write(_keyline())

    def _removekey(self):
        removal_lines = []
        new_authorized_keys = "%s.new" % Access.authorized_keys_file
        # Transfer the good lines
        with open(Access.authorized_keys_file, 'r') as old_auth:
            with open(new_authorized_keys, 'w') as new_auth:
                for line in old_auth:
                    if line == _keyline(): # line to be removed
                        continue
                    new_auth.write(line)
        # switch files
        import os
        os.rename(Access.authorized_keys_file, "%s~" %
                Access.authorized_keys_file)
        os.rename(new_authorized_keys, Access.authorized_keys_file)
