"""
Created on Sat Oct 14 18:53:08 2017

@author: ronaksharma
"""
# This file aims to run the diagonastic code for testing the different aspects of the ROV

#------------- MODULES USED-----------#

from time import sleep
import socket
#------------------------------------#

#HOST='192.168.1.5' # Defining the target
HOST='localhost'
PORT=8000      # Definig the target port 

instance=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP collection

def ThrusterConfiguration(position,speed):
    Configuration=str((str(position)+','+str(speed))).encode()
    return(Configuration)



# Do you want to test multiple thruster at the same time. If that, then you just 
#need to loop your arduino to wait for 2 sets of strings and that will be defined 
#by the a number that I might send at the end???\

loop_counter=0

while(loop_counter!='1'):
    
    System_Status=input('Which operation do you want to perform?\nNormal(Press 1)\nDiagonastic (Press 2)\n')

    if(System_Status=='1'):
        print('Performing normal operation...')

    elif(System_Status=='2'):
        thruster_position=input("Enter thruster values\n ").split()
        configurationString=ThrusterConfiguration(thruster_position,thruster_speed)
        instance.sendto((configurationString),(HOST,PORT))
    else:
        print('This is not a valid function')
        
    loop_counter=input('\nDo you want to continue\n Press 0\n')
    
