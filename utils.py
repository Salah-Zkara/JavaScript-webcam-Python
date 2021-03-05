from PIL import Image
from io import BytesIO
import base64
import numpy as np
import cv2 


def pil_image_to_base64(pil_image):
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue())


def base64_to_pil_image(base64_img):
    return Image.open(BytesIO(base64.b64decode(base64_img)))


def pil_to_opencv(PIL_img):
    pil_image = PIL_img.convert('RGB') 
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image
    

def opencv_to_pil(opencv_img):
    color_coverted = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)  

    return pil_image

