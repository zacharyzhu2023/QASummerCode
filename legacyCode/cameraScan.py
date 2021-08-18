# Program to go from a camera scna to QR code read

import cv2 # Module to allow for reading image/camera/video input
from pyzbar import pyzbar
from pyzbar.pyzbar import decode


# Source Code: https://www.youtube.com/watch?v=IOhZqmSrjlE&ab_channel=KostadinRistovski

def test1():
	cap = cv2.VideoCapture(0)
	cap.set(3, 100) # Set width (setting 3) to 100 pixels
	cap.set(4, 100) # Set height (setting 4) to 100 pixels

	camera = True # Make sure we're operating with camera mode
	while camera: # Ensure that we're in camera mode
		success, frame = cap.read() # Read in the camera results
		for code in decode(frame):
			print(code.type) # Indicate what kind of code was generated
			print(code.data.decode('utf-8')) # Decode the actually results of the camera scan
			print(code.data) # Decode the actually results of the camera scan
		cv2.imshow('Testing-code-scan', frame) # What the hell does this do?
		cv2.waitKey(1) # Delay 100ms before the next scan

test1()

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #3
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame

def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()

