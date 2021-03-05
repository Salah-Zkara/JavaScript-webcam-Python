import cv2
import numpy as np


class Process(object):
    def __init__(self):
        self.lower_skin = np.array([0,20,70], dtype=np.uint8)
        self.upper_skin = np.array([20,255,255], dtype=np.uint8)

    def GetImage(self,Image):
        self.image = Image
        
    
    def ProcessHand(self):
        rect = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(rect, self.lower_skin, self.upper_skin)
        self.mask = cv2.GaussianBlur(self.mask,(5,5),100)
        self.mask128 = image_resize( self.mask , 128 , 128 )


    def Predict(self,model):
        self.ProcessHand()
        self.image128 = img_to_sample(self.mask128)
        self.image128 = self.image128.reshape(1,128,128,1)
        self.y_hat = model.predict( self.image128 )
        self.label = np.argmax( self.y_hat )
        if self.y_hat[0][self.label] == 1.0:
            self.tlabel = -1
        else:
            self.tlabel = self.label


        




def process_image(img,kernel):
    img = cv2.resize(img, (128, 128))
    img = cv2.GaussianBlur(img,(5,5),0)
    _,img = cv2.threshold(img,80,255,cv2.THRESH_BINARY)
    
    im_floodfill = img.copy()
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    img = img | im_floodfill_inv
    
    
    img = img/255
    return img

def img_to_sample(img, kernel = None):
    img = img.astype(np.uint8)
    img = np.reshape(img, (128, 128))
    
    img = process_image(img, kernel)
    
    img = np.reshape(img, (128, 128, 1))
    return img


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)

    return resized
