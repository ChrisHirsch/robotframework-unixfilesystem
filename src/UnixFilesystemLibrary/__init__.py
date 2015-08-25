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
        logger.debug("HERE!")
        if not os.path.exists(path):
            raise Exception('Could not open file ' + path)
        return os.stat(path).st_uid

    def get_owner_from_path(self, path):
        """
        Return the owner (name) of the path
        """
        logger.debug("get_owner_from_path")
        hope = self.get_uid_from_path(path)
        logger.debug("hope=" + str(hope))
        morehope = pwd.getpwuid(hope)
        logger.debug("morehope=" + str(morehope))

        return str(morehope.pw_name)

    def owner_from_path_should_match(self, owner, path):
        """
        Return True if the owner matches user name of the path
        """
        path_owner = self.get_owner_from_path(path)
        logger.debug("path_owner=" + str(path_owner))
        logger.debug("I return this=" + str(owner == path_owner))

        return owner == path_owner

    def get_permissions_from_path_as_octal(self, path):
        """
        Returns the octal values of the path
        """
        info = os.lstat(path)
        logger.debug("info=" + str(info))
        myoct = oct(info.st_mode & 0777)
        logger.debug("oct info=" + str(myoct))
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
        Returns True if the the octal values of the path mactches the mode. ie '0755'
        """
        info = os.lstat(path)
        logger.debug("info=" + str(info))
        myoct = oct(info.st_mode & 0777)
        logger.debug("oct info=" + str(myoct))
        logger.debug("mode =" + mode)
        return str(myoct) == str(mode)



