import cv2
import sys
import numpy as np
img = cv2.imread("qrdeneme.png")
if img is None:
    sys.exit("Could not read")
cv2.imshow("Display window", img)



#Translation
rows, cols,_ = img.shape
M = np.float32([[1,0,100],[0,1,50]]) #Translation Matrix
dst = cv2.warpAffine(img,M,(cols, rows)) #Third argument is the size of the output which is (width, height) = (columns, rows)
cv2.imshow("Translated image", dst)

#Rotation
M2 = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0), 45, 1) #Rotation Matrix
dst2 = cv2.warpAffine(img,M2,(cols,rows))
cv2.imshow("Rotated Image", dst2)

#Affine Transformation
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])
M3 = cv2.getAffineTransform(pts1,pts2) #Affine Transformation Matrix
dst3 = cv2.warpAffine(img,M3,(cols,rows))
cv2.imshow("Affine Transformated Image", dst3)

#Copying with imwrite when pressing a key
k = cv2.waitKey(0)
if k == ord("s"):
    cv2.imwrite("qrdeneme_copy.png", img)
cv2.destroyAllWindows()