import WebGUI
import HAL
import cv2
from math import exp, copysign
# Enter sequential code!
i=0
velocity = 1
kp = 0.008
ki = 0.000005
kd = 0.003
err_ant = 0
P,I,D = 0,0,0
HAL.setV(velocity)
while True:
   # Enter iterative code!
   img = HAL.getImage()
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   red_mask = cv2.inRange(hsv, (0,125,125), (30,255,255))
   contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   M = cv2.moments(contours[0])
   if M["m00"] != 0:
       cX = M["m10"] / M["m00"]
       cY = M["m10"] / M["m00"]
   else:
       cX, cY = 0, 0
  
   if  cX > 0:
       err = 320 - cX
       abs_err= abs(err)


       if abs_err<30:
           v = 8 
       elif abs_err < 60:
           v = 3 
       elif abs_err < 200:
           v = 2
       elif abs_err < 250:
           v = 1


       # Proporcional
       P = kp*err


       # #Integral
       # if abs_err < 45:
       #     I = 0
       # else:
       #     I = I + ki*err


       #Derivativo
       D = kd*(err-err_ant)
       err_ant = err
       HAL.setV(v)
       HAL.setW(P+D) #I #D
       #print(f'Integral: {I}, Proporcional: {P}, Derivativo: {D}')
       #print(f'ERROR: {err_ant}, {err}, {err-err_ant}')
       #print(f'ERROR: {err}, VELOCIDAD: {v}, GIRO: {w}')
   WebGUI.showImage(red_mask)
   i = i+1

