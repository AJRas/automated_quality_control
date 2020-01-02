import colorsys
import numpy as np
import cv2
from PIL import Image
import random

#RGB
#print("WHITE: ",colorsys.rgb_to_hsv(255,255,255))
#print("BLACK: ",colorsys.rgb_to_hsv(0,0,0))
#print("RED: ",colorsys.rgb_to_hsv(255,0,0))
#print("GREEN: ",colorsys.rgb_to_hsv(0,255,0))
#print("BLUE: ",colorsys.rgb_to_hsv(0,0,255))
#print("YELLOW: ",colorsys.rgb_to_hsv(255,255,0))
#print("MAGENTA: ",colorsys.rgb_to_hsv(255,0,255))
#print("cyan: ",colorsys.rgb_to_hsv(0,255,255))

#GREY: (0.0, 0.0, 85-170) with a certain delta
#WHITE:  (0.0, 0.0, 255)
#BLACK:  (0.0, 0.0, 0)
#RED:  (0.0, 1.0, 255)
#GREEN:  (0.3333333333333333, 1.0, 255)
#BLUE:  (0.6666666666666666, 1.0, 255)
#YELLOW:  (0.16666666666666666, 1.0, 255)
#MAGENTA:  (0.8333333333333334, 1.0, 255)
#CYAN:  (0.5, 1.0, 255)

cv2.destroyAllWindows() #Program will shut down if not shut down by q exit

cap = cv2.VideoCapture(0) #Sets what device to use for pictures

cv2.waitKey(5000)
ret, frame = cap.read()
cv2.imshow('frame1', frame)

cv2.imwrite('frame1.jpg', frame)
im = Image.open('frame1.jpg')

print(im.format, im.size, im.mode)

pixel_array = [0 for x in range((im.size[1])*(im.size[0]))] #Long 1D array

#print(pixel_array)

for y in range(im.size[1]): #Assigns picture pixels to an array
    for x in range(im.size[0]):
         coordinate = (x, y)
         index = x+(y*640)
         pixel_array[index] = im.getpixel(coordinate)
         check = pixel_array[index]
         if check[0] <= 46 and check[1] <= 46 and check[2] <= 46: #black detection
              RGB1 = (0, 0, 0)
         elif check[0] >= 230 and check[1] >= 230 and check[2] >= 230: #white detection
              RGB1 = (255, 255, 255)
         else:
              HSV = colorsys.rgb_to_hsv(check[0], check[1], check[2])
              RGB1 = colorsys.hsv_to_rgb(HSV[0], HSV[1], 255)
         RGB2 = int(RGB1[0]), int(RGB1[1]), int(RGB1[2])
         pixel_array[index] = RGB2
print("x is ",im.size[0])
print("y is ",im.size[1])
img = Image.new('RGB', im.size, color='red')

pixel_array1 = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for x in range((im.size[0])*(im.size[1]))] #Long 1D array
img.putdata(pixel_array1)
img.save('generated.jpg')

#while(True): #Adds a stop so the program doesn't immediately close everything
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

cap.release()
cv2.destroyAllWindows()