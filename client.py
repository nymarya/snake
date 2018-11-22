import sys
from PyQt4 import QtGui, QtCore
from threading import Thread
from client_socket import Listener
from socket import AF_INET, socket, SOCK_STREAM

class SnakeClient(QtGui.QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    prevKey = None
    def __init__(self, socket_from_client):
        super(SnakeClient, self).__init__()
        
        self.initUI()
        self.client_socket = socket_from_client
        self.thread = Listener(socket=self.client_socket)
        self.connect(self.thread, QtCore.SIGNAL("output(int, int, PyQt_PyObject)"), self.addText)
        
    def initUI(self):      
        """ Init components from User Interface"""
        self.setGeometry(500, 300, 600, 500)
        self.setWindowTitle('Snake')
        self.keyPressed.connect(self.on_key)
        self.viewer = QtGui.QLabel()
        self.viewer.setFixedSize(600, 400)
        pixmap = QtGui.QPixmap(self.viewer.size())
        pixmap.fill(QtGui.QColor(0, 0, 0))
        self.viewer.setPixmap(pixmap)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.viewer, 1, 0, 1, 1)
        self.setLayout(layout)
        self.show() 

    def addText(self, x, y, text):
        """ Add text to the screen when the thread Listener sends
            a signal
        """
        pixmap = self.viewer.pixmap()
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.setFont(QtGui.QFont('Decorative', 10))
        p= QtCore.QPointF(10*y, 10*x)
        if(text == ' '):
            # Erase the snake's tail
            msg = '#'
            painter.setPen(QtGui.QColor(0, 0, 0))
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y)-1, (10*x)-1)
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y), (10*x)-1)
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y)-1, (10*x))
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y)+1, (10*x)+1)
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y)+1, (10*x))
            painter.drawText(p, msg)
            p= QtCore.QPointF((10*y), (10*x)+1)
        else:
            msg = text
        painter.drawText(p, msg)
        painter.end() 
        self.viewer.update()

    def keyPressEvent(self, event):
        """Listen to the key press from client.
        """
        super(SnakeClient, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):
        """ If the key pressed is different from the one stroked previously,
            send the signal to the server.
        """
        key = event.key()
        if event.key() == QtCore.Qt.Key_Q:
            print ("Killing")
            self.deleteLater() 
            server.close() 
        else:
            # if key pressed changes
            if( key != self.prevKey):
                self.client_socket.send(bytes(str(key), "utf-8"))
                self.prevKey = key
                #print (event.key())
                
        
def main():
    #################################
    ## Begin client code
    server = socket(AF_INET, SOCK_STREAM) 
    if len(sys.argv) != 3: 
        print ("Correct usage: script, IP address, port number")
        exit() 
    IP_address = str(sys.argv[1]) 
    Port = int(sys.argv[2]) 
    server.connect((IP_address, Port))
    app = QtGui.QApplication(sys.argv)
    ex = SnakeClient(socket_from_client=server)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()