"""Watch class"""
from time import time


class Watch():
    """This is the watch class"""
    def __init__(self, logger, sock, addr):
        self._sock = sock
        self._logger = logger
        self._addr = addr
        self._timeout = time()

    def _loginfo(self, text):
        """This method log information msgs"""
        self._logger.info('Watch({}): {}'.format(self._addr, text))

    def _logerror(self, text):
        """This method log critical msgs"""
        self._logger.critical('Watch({}): {}'.format(self._addr, text))

    def get_addr(self):
        """speed getter"""
        return self._addr

    def check_timeout(self):
        """Check auth timeout"""
        return

    def handle_data(self, data):
        """This method handle data"""
        self._loginfo(data)

    def _sends(self, datastr):
        """This method send string"""
        self._send(datastr.encode('utf-8'))

    def _send(self, data):
        """This method send bytes"""
        self._sock.send(data)

    def close(self):
        """close all resources"""
        return
