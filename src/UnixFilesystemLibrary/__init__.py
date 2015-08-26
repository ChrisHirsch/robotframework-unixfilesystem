import os
import pwd
from robot.api import logger

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class UnixFilesystemLibrary(object):

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def get_uid_from_path(self, path):
        """
        Return the UNIX User ID of the path
        """
        if not os.path.exists(path):
            raise Exception('Could not open file ' + path)
        return os.stat(path).st_uid

    def get_owner_from_path(self, path):
        """
        Return the owner (name) of the path
        """
        return str(pwd.getpwuid(self.get_uid_from_path(path)).pw_name)

    def owner_from_path_should_match(self, owner, path):
        """
        Return True if the owner matches user name of the path
        """
        path_owner = self.get_owner_from_path(path)

        return owner == path_owner

    def get_permissions_from_path_as_octal(self, path):
        """
        Returns the octal values of the path
        """
        # Use lstat instead of stat so that we get info about the symlink itself
        # and not what the symlink points to
        info = os.lstat(path)
        myoct = oct(info.st_mode & 0777)
        return str(myoct)

    def get_permissions_from_path_as_list(self, path):
        """
        Returns a list of modes from the lstat
        """
        raise NotImplementedError("Sorry, we currently don't support \
                                  permissions as a list. Feel free to implement\
                                  and submit a pull request")

    def permissions_from_path_should_match(self, path, mode):
        """
        Returns True if the the octal values of the path mactches the mode.
        ie '0755'
        """
        info = os.lstat(path)
        myoct = oct(info.st_mode & 0777)
        return str(myoct) == str(mode)
