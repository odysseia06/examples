import numpy as np
import cv2 as cv
img = cv.imread('nature_view.jpg')
px = img.item(10, 10, 2)

def change_color(img, x1, y1, x2, y2, color, type):
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            img.itemset((i , j, type), color)

change_color(img, 10, 10, 300, 300, 50, 2)
cv.imwrite("nature_view_edited.jpg", img)
