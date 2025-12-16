import WebGUI
import HAL
import Frequency
from math import sqrt, atan, pi, cos, sin
from numpy import linspace
import cv2
import time
#Inicializar variables
GoX, GoY, GoZ = 32.5, -35 , 4
HAL.takeoff(GoZ)
MiX, MiY, MiZ = HAL.get_position()
Yaw = atan((GoY-MiY)/(GoX-MiX))
D = sqrt((MiX-GoX)**2+(MiY-GoY)**2)
#SOLO AL INICIO
HAL.set_cmd_pos(GoX, GoY, GoZ, Yaw)
while D > 0.5:
   MiX, MiY, MiZ = HAL.get_position()
   D = sqrt((MiX-GoX)**2+(MiY-GoY)**2)
print('Llegué :)')


face_detector = cv2.CascadeClassifier('/resources/exercises/rescue_people/haarcascade_frontalface_default.xml')


# Parámetros de la espiral
a = 1      
b = 2    
theta_max = 8 * pi
particiones = 80
thetas = linspace(0, theta_max, particiones)
pos_survivor = []
for i, theta in enumerate(thetas):
   r = a + b * theta/(2*pi)
   GoX_E = r * cos(theta) + GoX
   GoY_E = r * sin(theta) + GoY
   MiX, MiY, MiZ = HAL.get_position()
   Yaw = atan((GoY_E-MiY)/(GoX_E-MiX))
   D = sqrt((MiX-GoX_E)**2+(MiY-GoY_E)**2)
   HAL.set_cmd_pos(GoX_E, GoY_E, 4, Yaw)
   while D > 0.05:
       D = sqrt((MiX-GoX_E)**2+(MiY-GoY_E)**2)
       MiX, MiY, MiZ = HAL.get_position()
   image = HAL.get_ventral_image()
   WebGUI.showImage(image)
   survivor_detected = False
   already_detected = False
   for angle in [0, 45, -45, 90, -90, 135, -135, 180]:
       h, w = image.shape[:2]
       rot_c= (h/2, w/2)
       rot_m = cv2.getRotationMatrix2D(rot_c , angle, 1)
       rotated_image = cv2.warpAffine(image, rot_m, (w, h))
       rotated_gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
       #WebGUI.showImage(rotated_gray)
       # scaleFactorn cambiar en función de la altura que lleve el dron
       faces = face_detector.detectMultiScale(rotated_gray, scaleFactor = 1.02, minNeighbors=2)
       if len(faces)>0:
           MiX, MiY, _ = HAL.get_position()
           for pos in pos_survivor:
               D = sqrt((MiX-pos[0])**2+(MiY-pos[1])**2)
               if D < 3.8:
                   already_detected = True
                   break
           if not already_detected:
               pos_survivor.append((MiX, MiY))
               survivor_detected = True
               break
       if already_detected:
           break
   if survivor_detected:
       print(f' Nuevo superviviente en: x={pos_survivor[-1][0]}, y={pos_survivor[-1][1]}')
   print(f"Progreso espiral {(i+1)/particiones*100:.2f} %")
print('Fin espiral')
print(f"Encontrado {len(pos_survivor)}")
print(pos_survivor)


#Código de vuelta
HAL.set_cmd_pos(0, 0, 4, Yaw)
D = sqrt((MiX-0)**2+(MiY-0)**2)
while D > 0.05:
   MiX, MiY, MiZ = HAL.get_position()
   D = sqrt((MiX-0)**2+(MiY-0)**2)
HAL.land()
print('Vuelta a casa ;)')
