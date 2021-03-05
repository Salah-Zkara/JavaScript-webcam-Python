from sys import stdout
import logging
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from Process import Process
import cv2 
#import tensorflow as tf
#from tensorflow import keras
import base64
from utils import base64_to_pil_image, pil_image_to_base64, pil_to_opencv,opencv_to_pil


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
#process = Process()
#mymodel = keras.models.load_model('./models/My_model-FG.ML')
font = cv2.FONT_HERSHEY_SIMPLEX


@socketio.on('input image', namespace='/flask')
def test_message(input):
    input = input.split(",")[1]

    input_img = base64_to_pil_image(input)

    img = pil_to_opencv(input_img)

    #process.GetImage(img)
    #process.Predict(mymodel)
    #img = process.mask

    cv2.imshow("Square-mask",img)
    if cv2.waitKey(10)==27:
        cv2.destroyAllWindows()
        return -1

    #retval, buff = cv2.imencode('.jpg', img)
    #jpg_as_text = base64.b64encode(buff)




    #image_data = "data:image/jpeg;base64," + str(jpg_as_text).split("'")[1]

    #process.tlabel

    emit('out-image-event', {'image_data':image_data}, namespace='/flask')


    emit('out-image-event', {'label':str(-1)}, namespace='/flask')


@app.route('/')
def index():
    return render_template('index.html')




if __name__ == '__main__':
    socketio.run(app)
    

