from .database import Database

class Access(Database):
    """ All classes that provide ssh access modification are derived from this
    one.

    This class should not be used directly, it only provides special *add()*,
    *remove()* functions which are using the unimplemented *_keyline()*
    function.
    """

    def __init__(self, id, pubkey):
        super().__init__()
        self.c_id = id
        self.c_pubkey = pubkey

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
        cls.create(attr)

    def remove(self):
        """ This method removes the object from database and authorized_keys.
        """
        super().remove()
