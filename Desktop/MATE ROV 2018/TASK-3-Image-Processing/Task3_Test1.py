import sys
import os
from math import *
from PyQt4 import QtGui, QtCore

# 
#https://stackoverflow.com/questions/11790504/about-a-pyqt-example-program
#I THINK I SHOULD CREATE SEPRATE BOXES FOR PROCESS INFORMATION AND SEND INFORMATION
class Example(QtGui.QWidget):  
      
    def __init__(self):
        super(Example, self).__init__()
         
        self.initUI()
        self.RequiredDistance=480
        self.y_cordinate=0
        self.x_cordinate=0
        self.X2=0
        self.Y2=0
        self.X_Coordinate=0
        
        self.setGeometry(300, 200, 1000, 500)
        self.setWindowTitle('TASK 3')  
        self.buttonStore1()
        self.btn.clicked.connect(self.StoreValue1)
        self.btn1.clicked.connect(self.StoreValue2)
        self.btn2.clicked.connect(self.Calculate)
        self.show()
    
    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()
        current=QtGui.QWidget.mapFromGlobal(self,cursor.pos())
        self.x_cordinate = current.x()
        self.y_cordinate = current.y()
    
    def buttonStore1(self):
        self.btn=QtGui.QPushButton("R",self)
        self.btn.resize(50,50)
        self.btn.move(100,50)
        self.btn.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
        
        self.btn1=QtGui.QPushButton("P",self)
        self.btn1.resize(50,50)
        self.btn1.move(200,50)
        self.btn1.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
   
        self.btn2=QtGui.QPushButton("CALCULATE",self)
        self.btn2.resize(100,50)
        self.btn2.move(500,20)
        self.btn2.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
        self.show()

    def initUI(self):                       
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)
        
    def Calculate(self): # Assumes that the x-cordinate is constant
        objectDistance=(self.Y2-self.Y1)
#       print(objectDistance)
        actualDistance=150
        scale=actualDistance/(objectDistance)
        X_ReferenceObject=self.X2
        self.X_Coordinate = (self.RequiredDistance/scale)+ X_ReferenceObject
        print(self.X_Coordinate)
#        QtGui.QWidget.update(self,self.X2,self.Y2, self.rect().width() -self.X_Coordinate , self.Y2)
        QtGui.QWidget.update(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("T_L.png")
        painter.drawPixmap(10, 100,772,248, pixmap)
#        painter.drawPixmap(self,10, pixmap)
        pen = QtGui.QPen(QtCore.Qt.blue, 3)
        painter.setPen(pen)
        painter.drawLine(self.X2,self.Y2, self.X_Coordinate , self.Y2)
        
        pen2 = QtGui.QPen(QtCore.Qt.green, 3)
        pen2.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen2)
        painter.drawLine(self.X_Coordinate, self.Y2, self.X_Coordinate, 100)
        painter.drawLine(self.X_Coordinate, self.Y2, self.X_Coordinate, 400)
        #Change the coordinate to the one required


    def StoreValue1(self):
        self.Y1=self.y_cordinate
        self.X1=self.x_cordinate
        print("Value 1 Stored",self.Y1,self.X1) 
    def StoreValue2(self):
        self.Y2=self.y_cordinate
        self.X2=self.x_cordinate
        print("Value 2 Stored",self.Y2,self.X2)


def main():        
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

