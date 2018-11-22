import sys
from PyQt4 import QtGui, QtCore
from threading import Thread
from teste2 import Listener
from socket import AF_INET, socket, SOCK_STREAM

class Example(QtGui.QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    prevKey = None
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 9000))
        self.thread = Listener(socket=self.client_socket)
        self.connect(self.thread, QtCore.SIGNAL("output(int, int, PyQt_PyObject)"), self.addText)
        
    def initUI(self):      

        self.text = u'a'

        self.setGeometry(100, 300, 600, 600)
        self.setWindowTitle('Draw text')
        self.keyPressed.connect(self.on_key)
        self.viewer = QtGui.QLabel()
        self.viewer.setFixedSize(500, 500)
        self.show()

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
    def drawText(self, event, qp):
      
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        p= QtCore.QPointF(10.0, 10.0)
        qp.drawText(p, self.text)  

    def addText(self, x, y, text):
        print("tentenado")
        pixmap = self.viewer.pixmap()
        painter = QtGui.QPainter()
        painter.begin(self)
        p= QtCore.QPointF(10.0+x, 10.0+y)
        painter.drawText(p, text)
        painter.end() 

    def keyPressEvent(self, event):
        super(Example, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):  # this is called whenever the continue button is pressed
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
                print (event.key())
                
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()