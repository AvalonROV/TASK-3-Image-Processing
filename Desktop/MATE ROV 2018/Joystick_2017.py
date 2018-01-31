#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 
In this example, we position two push
buttons in the bottom-right corner 
of the window. 
author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4.QtGui import*
from PyQt4.QtCore import *
import pygame
import socket
from time import sleep

#HOST = 'localhost'
HOST = '192.168.1.5'
send_port = 8000      # Defining the target send_port
recieve_port = 12345  # Defining the target recieve_port

send_scoket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP collection

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
recieve_socket.bind(("", recieve_port))


pygame.init()
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()

app = QApplication(sys.argv)

LED1 = 0
LED2 = 0

class Window(QWidget):
    
    def __init__(self):
        super(Window, self).__init__() #WHY NOT SETTING THE DIMENSIONS OR COLOUR ETC
                                        # WHAT DOES SUPER DO
        
        self.initUI()
        self.string_formatter()
        
        # ------THREADING-----#
        self.thread = Worker()
        self.connect(self.thread, SIGNAL('Hello'), self.information)
        self.thread.start()

        recieve_socket.setblocking(0)
        
                #------UDP Connection-----#
        #recieve_socket.settimeout(1)
        #while (True):
        #    send_scoket.sendto(("UDP_auth".encode()), (HOST, send_port))
        #    print('sending...')
        #    try:
        #        if (recieve_socket.recv(1024).decode() == 'auth_acknowledged'):
        #            break
        #    except:
        #        pass
                # sleep(5)
        #print('Connected!')

    def initUI(self):

        title1_font = QFont("Arial", 16, QFont.Bold)
        #title2_font = QFont("Arial", 10, QFont.setUnderline(True))

        application_title = QLabel()                        #Create label
        application_title.setText("ROV Control Interface")  #Set Text
        application_title.setFont(title1_font)
        application_title.setAlignment(Qt.AlignCenter)      #Set Allignment

        self.LEDs_label = QLabel()
        self.LEDs_label.setText("LEDs")

        self.led1_label = QLabel()
        self.led1_label.setText("Spectrum")
        self.led2_label = QLabel()
        self.led2_label.setText("Lights")

        self.led1_indicator = QLabel()
        self.led2_indicator = QLabel()
        self.red_circle_indicator = QPixmap('red_circle.png')# Store the image in one file
        self.green_circle_indicator = QPixmap('green_circle.png')
        self.led1_indicator.setPixmap(self.red_circle_indicator)
        self.led2_indicator.setPixmap(self.red_circle_indicator)

        self.recieved_string_label = QLabel()
        self.recieved_string_label.setText("String Recieved from ROV")
        self.recieved_string_txtbox = QTextEdit()
        self.recieved_string_txtbox.setReadOnly(True)#?????????
        self.complete_recieved_string = '' #????????

        self.user_input = QTextEdit()

        
        ## WHY IS THIS IMPORTANT TO CREATE A LAYOUT AND WHY NOT FOR THE LED_RED LABEL_SPECTRUM
        
        vbox = QVBoxLayout() #Create layout container
        vbox.addWidget(application_title)

        vbox.addWidget(self.LEDs_label)
        #-------------------------#
        
        ## ARE YOU USING THIS TO ARRANGE THE BOXES RATHER THAN USING DIMENSIONS SPECIFICALLY
        LEDs_hbox = QHBoxLayout()
        LEDs_hbox.addWidget(self.led1_label)
        LEDs_hbox.addWidget(self.led1_indicator)
        LEDs_hbox.addWidget(self.led2_label)
        LEDs_hbox.addWidget(self.led2_indicator)

        vbox.addLayout(LEDs_hbox)

        vbox.addWidget(self.recieved_string_label)
        #vbox.addWidget(self.recieved_string_txtbox)

        #vbox.addWidget(self.user_input)
        recieved_string_box = QHBoxLayout()
        recieved_string_box.addWidget(self.recieved_string_txtbox)
        recieved_string_box.addWidget(self.user_input)

        vbox.addLayout(recieved_string_box)# IS THE VERTICAL DISTANCE DEFINED IN THE ORDER THEY ARE DECLARED

        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()

    #------------What is to follow should be moved into a seprate file----------------------------
    def string_formatter(self):
        # ------ Storing the values from the different axis on joystick------#
        self.X_Axis = my_joystick.get_axis(0)  # X_Axis- Axis 0
        self.Y_Axis = my_joystick.get_axis(1)  # Y_Axis - Axis 1
        self.Throttle = my_joystick.get_axis(2)
        self.Yaw = my_joystick.get_axis(3)
        self.Rudder = my_joystick.get_axis(4)
        self.funnel_CW_button = my_joystick.get_button(4)  # Button 5
        self.funnel_CCW_button = my_joystick.get_button(5)  # Button 6
        self.arm_open_button = my_joystick.get_button(6)  # Button 7
        self.arm_close_button = my_joystick.get_button(7)  # Button 8
        self.LED1_button = my_joystick.get_button(10)  # Button SE
        self.LED2_button = my_joystick.get_button(11)  # Button ST
        self.BT_button1 = my_joystick.get_button(0)
        self.BT_button2 = my_joystick.get_button(1)
        self.BT = 0

        if(self.BT_button1 == 1):
            self.BT = 1
        elif(self.BT_button2 == 1):
            self.BT = 2

        # self.Roll= my_joystick.get_button(0)

        self.funnel = 0
        self.arm = 0
        global LED1
        global LED2

        # ------ Thrusters Power
        self.power = 0.4
        self.fwd_factor = 400 * self.power
        self.side_factor = 400 * self.power
        self.yaw_factor = 200  # minimum drag

        # Account for double power in case of diagonals
        if ((self.X_Axis > 0.1 and self.Y_Axis < -0.1) or
                (self.X_Axis < -0.1 and self.Y_Axis > 0.1) or
                (self.X_Axis < -0.1 and self.Y_Axis < -0.1) or
                (self.X_Axis > 0.1 and self.Y_Axis > 0.1)):
            self.fwd_factor = 200 * self.power
            self.side_factor = 200 * self.power
        
        #--------DID WE ASSUME A DEADZONE AROUND 1500-------------#
        #--------Less than 1500 is thrusters spinning in the opposite directions----#
        #----COULD YOU WRITE A DOCUMENT ABOUT IT AS MIGHT BE HELPFUL FOR THE COMING TEAM MEMBERS----------#
        #CAN YOU USE AN EXAMPLE OF MOVING FORWARD(SO JUST Y AXIS) AND SHOW THE VALUES OF THRUSTER. HOW CAN FRONT MOTORS OPERATE IN OPPOSITE DIRECTION#
        self.fwd_left_thruster = int(
            1500 - self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.fwd_right_thruster = int(
            1500 + self.fwd_factor * self.Y_Axis + self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.bck_left_thruster = int(
            1500 - self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.bck_right_thruster = int(
            1500 + self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)

        self.front_thruster = int(1500 + self.fwd_factor * self.Rudder)
        self.back_thruster = int(1500 + self.fwd_factor * self.Rudder)

        # ------Pitching code------
        if(self.Throttle>0.1 or self.Throttle<-0.1):
            self.front_thruster = int(1500 - self.fwd_factor * self.Throttle)
            self.back_thruster = int(1500 - self.fwd_factor * self.Throttle)
        # -------------------------


        if (self.funnel_CW_button == 1):
            self.funnel = 1
        elif (self.funnel_CCW_button == 1):
            self.funnel = 2

        if (self.arm_open_button == 1):
            self.arm = 1
        elif (self.arm_close_button == 1):
            self.arm = 2

        if (self.LED1_button == 1):
            sleep(0.2)# WHY THESE DELAYS??????????
            if (LED1 == 1):
                LED1 = 0
                self.led1_indicator.setPixmap(self.red_circle_indicator)
            else:
                LED1 = 1
                self.led1_indicator.setPixmap(self.green_circle_indicator)

        if (self.LED2_button == 1):
            sleep(0.2)
            if (LED2 == 1):
                LED2 = 0
                self.led2_indicator.setPixmap(self.red_circle_indicator)
            else:
                LED2 = 1
                self.led2_indicator.setPixmap(self.green_circle_indicator)

        self.stringToSend = str([self.fwd_left_thruster, self.front_thruster, self.fwd_right_thruster,
                                 self.bck_right_thruster, self.back_thruster, self.bck_left_thruster,
                                 self.arm, self.funnel, self.BT_button1, LED2, self.BT])
        print(self.stringToSend)

    def information(self):
        # self.comma=","
        # ----- Collecting Self Parameters of Joystick----#
        name_joystick = my_joystick.get_name()  # Collects the pre-defined name of joystick
        number_axes = my_joystick.get_numaxes()  # Collects the pre-defined number of axis
        number_buttons = my_joystick.get_numbuttons()  # Collects the pre-defined number of buttons
        #self.txt1.setText(str(name_joystick))  # Displaying the information
        #self.txt2.setText(str(number_axes))  # in the required textboxes
        #self.txt3.setText(str(number_buttons))
        send_scoket.sendto((self.stringToSend.encode()), (HOST, send_port))  # The thing that we send
        #??????????????-----IS THIS FOR THE ARDUINO------???????????????#
        
        try:
            recieved_string = recieve_socket.recv(1024).decode()
            self.complete_recieved_string += recieved_string + '\n'
            self.recieved_string_txtbox.setText(self.complete_recieved_string)
            #print(self.complete_recieved_string)
        except:
            pass ## DOES THIS IGNORE THE STATEMENT?????

        self.string_formatter()  # Calling the thruster value


#???????CAN THREAD BE IMPLEMENTED IN ANY OTHER FUNCTION AND ALSO CONFIRM WITH HIM THE WORKING OF THE THREAD???????#
class Worker(QThread):

    def __init__(self):
        QThread.__init__(self, parent=app)

    def run(self):
        EXIT=False
        while not EXIT:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    EXIT=True
            self.emit(SIGNAL('Hello'))
            clock.tick(30) #This determines how fast the frames change per second
            #time.sleep(1)
        pygame.quit() # This is used to quit pygame and use any internal program within the python
        quit()

def main():
    
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()