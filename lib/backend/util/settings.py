from os.path import join, expanduser, isfile

class _Wrapper:
    @property
    def DEFAULT_CONFIG(self):
        """ Where the default config file comes from """
        config_paths = []
        config_paths.append(join(expanduser("~"), "ctlweb.conf"))
        config_paths.append("/etc/ctlweb.conf")

        for path in config_paths:
            if isfile(path):
                return path
        return None

DEFAULT_CONFIG = _Wrapper().DEFAULT_CONFIG
