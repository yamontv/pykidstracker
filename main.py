"""This module daemonize everything"""
import os
import signal
from threading import Event
import logging
import configparser
import daemon
import daemon.pidfile

from web_server import WebServer
from sk_server import SocketServer


class MainAPP():
    """This class does blah blah"""
    def __init__(self):
        self._stop_request = Event()

    def sigint_handler(self, _signum, _frame):
        """This method does blah blah"""
        self._stop_request.set()

    def work(self):
        """This method does blah blah"""
        #open config
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('config.ini')

        #setup logger to file
        logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler('log.log', mode='w')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

        logger.info("MainAPP Started")
        #start everything
        sk_server = SocketServer(config, logger)
        sk_server.start()
        web_server = WebServer(config)
        web_server.start()
        #wait for stop
        while not self._stop_request.wait(timeout=5):
            pass
        #stop everything
        sk_server.stop()
        web_server.stop()
        logger.info("MainAPP Stopped")

    def run(self):
        """This method does blah blah"""
        here = os.path.dirname(os.path.abspath(__file__))
        out = open('std.log', 'w+')

        context = daemon.DaemonContext(
            working_directory=here,
            stdout=out,
            stderr=out,
            pidfile=daemon.pidfile.PIDLockFile('pid.pid'))

        context.signal_map = {
            signal.SIGTERM: self.sigint_handler,
        }

        context.open()
        with context:
            self.work()


if __name__ == "__main__":
    APP = MainAPP()
    APP.run()
