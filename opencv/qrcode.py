import cv2
import qrcode
from random import randint
import numpy as np
'''
trial = "1"
for i in range(250):
    trial = trial + "1"
print(trial)
'''
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)


min = 100
max = 1000
random_number = randint(min, max)
random_number = str(random_number)
qr.add_data(random_number)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrdeneme.png")

file = cv2.imread("qrdeneme.png")


def display(im, bbox):
    n = len(bbox[0])
    for j in range(n):
        cv2.line(im, tuple((bbox[0])[j][0]), tuple((bbox[0])[ (j+1) % n][0]), (255,0,0), 3)
    cv2.imshow("Results", im)

cv2.namedWindow("Rectified QRCode", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Rectified QRCode", 600, 600)
qrCodeDetector = cv2.QRCodeDetector()
val, pts, st_code = qrCodeDetector.detectAndDecode(file)

if len(val)>0:
    print("Decoded Data : {}".format(val))
    #display(file, pts)
    rectifiedImage = np.uint8(st_code)

    cv2.imshow("Rectified QRCode", rectifiedImage)

else:
    print("QR Code is not detected")
    cv2.imshow("Results", file)

cv2.waitKey(0)
cv2.destroyAllWindows()    
    



