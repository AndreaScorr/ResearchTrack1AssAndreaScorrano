from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
#R.location(300)
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
    

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def cicle(speed,seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = 2*speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    print(len(R.see()))
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
	    codeToken=token.info.code
	    print(token.dist)
    if dist==100:
	return -1, -1,-1
    else:
   	return dist, rot_y, codeToken




drive(60,5)

#turn(-10,12)
#print(R.see())
#inizialize the list of token 
tokens=[]

#this for is used to turn around itself and see the available tokens
for i in range(0,12):
	print(R.see(),'\n')
	turn(-10,1)
	for token in R.see(): #R.see return a list of tokens, the for loop scroll throught the list to see take the code of token
		if not token.info.code in tokens:
			tokens.append(token.info.code)
	

print('tokens')
print((tokens))

tokenToApproach=list(tokens) #this is the list of tokens that mast be closer to the gray area
tokenToAlignTogether=list(tokens) #this is the list of tokens that mast be aligned together
#both are copy of the original list, in order to not modify the original one

#this while is used to bring the golden box coser to the gray area
while not len(tokenToApproach)==0: #stop the while when there are no tokens anymore 
    
    dist, rot_y, codeToken = find_golden_token()
    if dist==-1: # if no token is detected, we make the robot turn 
	print("I don't see any token!!")
	turn(-10, 1) #turn a little bit on left
    elif dist <d_th: # if we are close to the token, we try grab it.
        print("Found it!",codeToken)
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            
            drive(-50,2)
            R.release()
            drive(-4,2)
            turn(-2,7)
            
            tokenToApproach.remove(codeToken)
            print('remaining tokens:',tokenToApproach)
        
	    
	else:
            print("Aww, I'm not close enough.")
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)
 
        

i=0
while not len(tokenToAlignTogether)==0:
    
    dist, rot_y,codeToken = find_golden_token()
    if dist==-1: # if no token is detected, we make the robot turn 
	print("I don't see any token!!")
	turn(-10, 1)
    elif dist <d_th: # if we are close to the token, we try grab it.
        print("Found it!")
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            turn(-21,2)
            drive(21,3)
            R.release()
            drive(-21,3)
            turn(21,2)
            i+=1
            tokenToAlignTogether.remove(codeToken)
            print('remaining tokens:',tokenToAlignTogether)
    
	    
	else:
            print("Aww, I'm not close enough.")
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)


print("work done!")
    
  
