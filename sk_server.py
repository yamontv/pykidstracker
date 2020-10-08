"""This module realise remote USB server"""
import socket
import select
from threading import Thread

from watch import Watch


class SocketServer(Thread):
    """This is the socket server class"""

    # maybe use socket.gethostname()?
    _HOST = '0.0.0.0'

    def __init__(self, config, logger):
        Thread.__init__(self)
        self._running = True
        self._logger = logger
        self._config = config
        self._sock = None
        self._users_list = {}
        self._order_number = 0
        self._init_socket()

    def _loginfo(self, text):
        """This method log information msgs"""
        self._logger.info('SocketServer(): {}'.format(text))

    def _logerror(self, text):
        """This method log critical msgs"""
        self._logger.critical('SocketServer(): {}'.format(text))

    def _init_socket(self):
        """This method open listening TCP socket"""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((self._HOST, int(self._config['main']['watch_port'])))
        self._sock.listen()

    def _run_once(self):
        """This method do the whole work"""
        # form socket list every time as list
        # could be moded in handlers
        socket_list = [self._sock]
        for sock in self._users_list:
            socket_list.append(sock)

        infds, _, _ = select.select(socket_list, [], [], 1)

        for fds in infds:
            if fds is self._sock:
                sock, addr = fds.accept()
                self._loginfo('Watch connected from {}'.format(addr))
                self._users_list[sock] = Watch(self._logger, sock, addr)
                continue

            if fds in self._users_list:
                user = self._users_list[fds]
            else:
                #unknows -> close
                self._logerror("uknown socket in list")
                socket_list.remove(fds)
                fds.close()
                continue

            data = fds.recv(1024)
            if not data:
                #closed
                self._loginfo('Watch({}) disconnected'.format(user.get_addr()))
                fds.close()
                socket_list.remove(fds)
                del self._users_list[fds]
                user.close()
            else:
                user.handle_data(data)

        # check timeouts
        for sock in list(self._users_list):
            user = self._users_list[sock]
            user.check_timeout()

    def _close(self):
        """This method destroy all server resources"""
        for sock in self._users_list:
            sock.close()
        self._sock.close()

    def run(self):
        """This method serves the server"""
        self._loginfo('Started')
        while self._running:
            self._run_once()
        self._loginfo('Stopped')

        self._close()

    def stop(self):
        """This method stops the server"""
        self._running = False
        self.join()
