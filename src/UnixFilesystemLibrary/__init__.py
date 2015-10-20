import os
import pwd
from robot.api import logger
from robot.utils import asserts

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class UnixFilesystemLibrary(object):

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def get_path(self, path):
        """
        Gets the path if possible even if a wildcard is supplied
        """
        if not os.path.exists(path):
            try:
                # Didn't find the path so try wildcard expansion next
                import glob
                globpath = glob.glob(path)
                globpath = globpath.pop()
                if not os.path.exists(globpath):
                   raise Exception('Could not open file ' + globpath)
                path = globpath
            except:
                raise Exception('Could not open file ' + path)
            # Assign
        return path



    def get_uid_from_path(self, path):
        """
        Return the UNIX User ID of the path
        """
        return os.stat(self.get_path(path)).st_uid

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
        asserts.fail_unless_equal(owner, path_owner, 'Owner From Path %s Should Match %s, but instead is %s' % (path, owner, path_owner))


    def get_permissions_from_path_as_octal(self, path):
        """
        Returns the octal values of the path
        """
        # Use lstat instead of stat so that we get info about the symlink itself
        # and not what the symlink points to
        info = os.lstat(self.get_path(path))
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
        info = os.lstat(self.get_path(path))
        myoct = oct(info.st_mode & 0777)
        asserts.fail_unless_equal(str(myoct), str(mode), 'Permissions from Path %s Should Match %s but instead are %s' % (path, mode, myoct))
