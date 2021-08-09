import cv2
import numpy as np

def detect_contour(file_path):
    # load image
    img = cv2.imread(file_path)
    # img = cv2.imread(r'houghlines5.jpg')

    img = cv2.resize(img, (1040, 1040))
    
    # Read the color image
    image = img
    
    # Make a copy
    new_image = image.copy()
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    im = img
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 180, 255, 0)
    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cnt = contours[4]
    # cv2.drawContours(img, [cnt], 0, (0,255,0), 3)

    # Display the grayscale image
    # cv2.imshow('Gray image', gray)  
    # cv2.waitKey(0) # Wait for keypress to continue
    # cv2.destroyAllWindows() # Close windows
    
    # Convert the grayscale image to binary
    ret, binary = cv2.threshold(thresh, 0, 255, 
    cv2.THRESH_OTSU)
    
    # Display the binary image
    # cv2.imshow('Binary image', binary)
    # cv2.waitKey(0) # Wait for keypress to continue
    # cv2.destroyAllWindows() # Close windows
    
    # To detect object contours, we want a black background and a white 
    # foreground, so we invert the image (i.e. 255 - pixel value)
    inverted_binary = ~binary
    # cv2.imshow('Inverted binary image', inverted_binary)
    # cv2.waitKey(0) # Wait for keypress to continue
    # cv2.destroyAllWindows() # Close windows
    
    # Find the contours on the inverted binary image, and store them in a list
    # Contours are drawn around white blobs.
    # hierarchy variable contains info on the relationship between the contours
    contours, hierarchy = cv2.findContours(inverted_binary,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE)
        
    # # Draw the contours (in red) on the original image and display the result
    # # Input color code is in BGR (blue, green, red) format
    # # -1 means to draw all contours
    with_contours = cv2.drawContours(image, contours, -1,(255,0,255),3)
    # cv2.imshow('Detected contours', with_contours)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # # Show the total number of contours that were detected
    # print('Total number of contours detected: ' + str(len(contours)))
    
    # # Draw just the first contour
    # # The 0 means to draw the first contour
    # first_contour = cv2.drawContours(new_image, contours, 1,(255,0,255),3)
    # cv2.imshow('First detected contour', first_contour)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Draw a bounding box around the first contour
    # x is the starting x coordinate of the bounding box
    # y is the starting y coordinate of the bounding box
    # w is the width of the bounding box
    # h is the height of the bounding box
    # x, y, w, h = cv2.boundingRect(contours[0])
    # cv2.rectangle(first_contour,(x,y), (x+w,y+h), (255,0,0), 5)
    # cv2.imshow('First contour with bounding box', first_contour)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Draw a bounding box around all contours
    rect = {}
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        
            # Make sure contour area is large enough
        if (cv2.contourArea(c)) > 200 and (cv2.contourArea(c)) < 1300:
            # print(i, cv2.contourArea(c))
            rect[i] = cv2.contourArea(c)
            cv2.rectangle(with_contours,(x,y), (x+w,y+h), (255,0,0), 5)
            
    # print(len(rect), max(rect.values()), min(rect.values()))


            
    # cv2.imshow('All contours with bounding box', with_contours)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    res = cv2.resize(with_contours, (640, 640))

    cv2.imwrite(r'static/out/out.png', res)

    # object_detection = 

    return res, len(rect)

if __name__ == "__main__":
    res, area = detect_contour(r"images\Bread_and_Tomato_on_Plate.jpg")