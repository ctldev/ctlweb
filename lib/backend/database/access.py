from .database import Database
from .pubkey import Pubkey
from util import Log


class Access(Database):
    """ All classes that provide ssh access modification are derived from this
    one.

    This class should not be used directly, it only provides special *add()*,
    *remove()* functions.
    """

    def __init__(self, id):
        super().__init__()
        self.c_id = id

    @classmethod
    def add(cls, attr):
        """ This method adds a new object to database and authorized_keys.

        attr is expected to be a dictionary.
        The attr are at least and have to be compatible with the create()
        attributes:
            * c_id
            * f_Pubkey_pubkey
        """
        Log.debug('Creating object with ssh access'
                  ' and granting access for public key.')
        return cls.create(attr)

    def add_key(self, pubkey):
        Pubkey.add(pubkey, self)

    def remove(self):
        """ This method removes the object from database and authorized_keys.
        """
        self.remove_keys()
        super().remove()

    def get_keys(self):
        """ Returns all Pubkey-Objects referencing this Access-Instance
        """
        return Pubkey.get_access_keys(self)

    def remove_keys(self):
        """ Removes all Pubkey-Objects referencing this Access-Instance
        """
        for key in self.get_keys():
            key.remove()

    def remove_key(self, pubkey):
        pubkey.remove()
