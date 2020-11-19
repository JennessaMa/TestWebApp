import cv2
import numpy as np

image  = cv2.imread("trap1.jpg")

cv2.imshow("Image", image)
scale_percent = 30 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)

blur = cv2.GaussianBlur(gray, (5,5), 0)
#cv2.imshow("blur", blur)

_, thresh = cv2.threshold(blur,110,255,cv2.THRESH_BINARY_INV)
#cv2.imshow("thresh", thresh)


contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
c = 0
for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1

mask = np.zeros((gray.shape),np.uint8)
cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)
#cv2.imshow("mask", mask)

out = np.zeros_like(gray)
out[mask == 255] = gray[mask == 255]
#cv2.imshow("New image", out)

blur = cv2.GaussianBlur(out, (5,5), 0)
#cv2.imshow("blur1", blur)

thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
#cv2.imshow("thresh1", thresh)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

numDrawn = 0
c = 0
for i in contours:
    area = cv2.contourArea(i)
    #500
    if area > 350:
        numDrawn += 1
        cv2.drawContours(image, contours, c, (0, 255, 0), 3)
    c+=1

print(numDrawn) #8

cv2.imshow("Final Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
