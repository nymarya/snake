from PyQt4 import QtCore
from socket import AF_INET, socket, SOCK_STREAM
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Listener(QtCore.QThread):

    def __init__(self, socket, parent = None):
    
        QtCore.QThread.__init__(self, parent)
        self.client_socket = socket
        self.exiting = False
        self.start()

    def __del__(self):

        self.exiting = True
        self.wait()
    def render(self, size, stars):
    
        self.start()
    
    def run(self):
        """ Thread receive the message and send the position of the
            components to the GUI
        """
        while not self.exiting:
            message = self.client_socket.recv(2048).decode("utf8")
            data = str(message).split(',')
            try:
                x = int(data[0])
                y = int(data[1])
                text = data[2]
                self.emit(SIGNAL("output(int, int, PyQt_PyObject)"),x,y,text)
            except:
                self.exiting = True


