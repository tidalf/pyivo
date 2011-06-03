import logging
import sys    

class Logger(object):

    """
    class implements logger functional
    """

    def __init__(self,log_file, level):
        logging.basicConfig(level = level,
                            format = '%(asctime)s %(levelname)s %(message)s',
                            filename = log_file,
                            filemode = 'a')
        self.name = None

    def add_new_logger(self, logger_name):
        """
        adds new loger name
        """
        self.name = logger_name

    def _whoami(self):

        """
        detects name of the caller function
        """           
        f_name = sys._getframe(2).f_code.co_name
        if self.name is not None:
            cls_name = self.name
        else:

            if 'self' in sys._getframe(2).f_locals:
                cls_name = sys._getframe(2).f_locals['self'].__class__.__name__
            else:
                cls_name = None
        return '{0}.{1}'.format(cls_name, f_name)

    def info(self, msg):

        """
        function writes info to log
        """
        logging.info('{0}: {1}'.format(self._whoami(),str(msg)))

    def debug(self, msg):

        """
        function writes debug to log
        """
        logging.debug('{0}: {1}'.format(self._whoami(),str(msg)))

    def warning(self, msg):

        """
        function writes warning to log
        """
        logging.warning('{0}: {1}'.format(self._whoami(),str(msg)))

    def error(self, msg):

        """
        function writes error to log
        """
        logging.error('{0}: {1}'.format(self._whoami(),str(msg)))        



