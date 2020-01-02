import cv2

cv2.destroyAllWindows() #Program will shut down if not shut down by q exit

cap = cv2.VideoCapture(0) #Sets what device to use for pictures

cv2.waitKey(50)
ret, frame = cap.read()
cv2.imshow('frame1', frame)

while(True): #Adds a stop so the program doesn't immediately close everything
    ret, frame = cap.read()
    cv2.imshow('frame1', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()