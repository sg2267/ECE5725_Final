#-*-coding: UTF-8-*-
import mediapipe
import cv2
import math
import json

from socket import *

udp = socket(AF_INET, SOCK_DGRAM)
targetAddr = ("10.49.71.170", 8080)
udp.bind(("", 3000))


# Hand Gesture
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

#Use CV2 to capture video
cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Loop Determint
loop = True

# Finger coordinate
top_coor = (0,0)
bottom_coor = (0,0)
diff_x = 0
diff_y = 0
angle_index = None
thumb_coor = (0,0)
little_coor = (0,0)
stop_x = 200
stop_y = 200
stop_sign = 0

# Determint output
output = ['nothing', 'nothing']

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

    # Loop to detect hands gestures
     while loop:
           #output = ['nothing', 'nothing']
           ret, frame = cap.read()
           # Set Frame size
           frame1 = cv2.resize(frame, (720, 640))
           
           #Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           
           key_in = cv2.waitKey(1) & 0xFF
           if (key_in == ord('w')):
               output[1] = 'up'  
           elif (key_in == ord('s')):
               output[1] = 'down'
           elif (key_in == ord('a')):
               output[1] = 'left'
           elif (key_in == ord('d')):
               output[1] = 'right'
           else:
               output[1] = 'nothing'
            
           #In case the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                  
                  #Below is Added Code to find and print to the shell the Location X-Y coordinates of Index Finger, Uncomment if desired
                  for point in handsModule.HandLandmark:
                      
                      normalizedLandmark = handLandmarks.landmark[point]
                      pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 720, 640)
                      if point == 8:
                          top_coor = pixelCoordinatesLandmark
                          #print("top", top_coor)
                    
                      if point == 5:
                          bottom_coor = pixelCoordinatesLandmark
                          #print("bottom", bottom_coor)
                          
                      if point == 4:
                          thumb_coor = pixelCoordinatesLandmark
                          
                      if point == 20:
                          little_coor = pixelCoordinatesLandmark
                        
                      if (top_coor != None and bottom_coor != None):
                          diff_x = top_coor[0] - bottom_coor[0]
                          diff_y = top_coor[1] - bottom_coor[1]
                          if (diff_x != 0):
                              angle_index = math.degrees(math.atan(diff_y / diff_x))
                          else:
                              angle_index = 90
                          print(angle_index)
                      if (thumb_coor != None and little_coor != None):
                          stop_x = thumb_coor[0] - little_coor[0]
                          stop_y = thumb_coor[1] - little_coor[1]
                      
                      if (stop_x < 40 and stop_y < 30) or (top_coor == None) or (bottom_coor == None):
                          stop_sign = 1
                          print("STOP")
                          output[0] = 'stop'
                      else:
                          stop_sign = 0
                      
                      # forward: x coor is close, y coor has a difference larger than 140
                      if (stop_sign == 0):
                          #if (diff_x < 30 and diff_y < -130):
                              #print("FORWARD")
                           #   output = 'forward'
                      
                          # right: y coor is close (smaller than 45), bottom x (120) larger than top x
                          if (diff_x < 0 and angle_index < 45):
                              print("RIGHT")
                              output[0] = 'right'
                      
                          # left: y coor is close (smaller than 45), top x (120) larger than bottom x
                          elif (diff_x > 0 and angle_index > -45):
                              print("LEFT")
                              output[0] = 'left'
                          else:
                              output[0] = 'forward'
                              print("FORWARD")
                      
                  
           print(output)
           # Socket Send Info
           data = json.dumps(output)
           #udp.sendto(output.encode("utf-8"), targetAddr)\
           udp.sendto(data.encode("utf-8"), targetAddr)
           #connect.close()
            
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", frame1);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              loop = False
              connect.close()
              cap.release()
              
              
              