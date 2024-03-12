import cv2
import numpy as np
from tensorflow.keras.models import load_model
import threading
import time
from main_func import AlphaBot
try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None
class AutonomousController:
    def __init__(self, model_path, **kwargs):
        self.bot = AlphaBot()
        self.running = True
        self.model = load_model(model_path)
        self.camera_initialized = False
        if Picamera2:
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (480, 320)}))
            self.picam2.start()
            self.camera_initialized = True
        
    def preProcess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) 
        img = cv2.GaussianBlur(img, (3, 3), 0) 
        img = cv2.resize(img, (200, 66))
        img = img / 255 
        return img

    def capture_and_predict(self):
        while True:
            if self.camera_initialized:
                im = self.picam2.capture_array()
                processed_img = self.preProcess(im)
                processed_img = np.expand_dims(processed_img, axis=0)
                steering_prediction = self.model.predict(processed_img)[0][0]
                print(steering_prediction)
                self.control_bot(steering_prediction)
                time.sleep(0.6) 

    def control_bot(self, steering_angle):
        if 0.94 <= steering_angle <= 1 or -1 <= steering_angle < -0.94:
            self.bot.right(70) 
        elif -0.47 < steering_angle < 0.47:
            self.bot.left(70)
        else:
            self.bot.forward(50)
    def run(self):
        control_thread = threading.Thread(target=self.capture_and_predict)
        control_thread.start()
    def stop(self):
        self.running = False
        self.bot.shutdown()

if __name__ == "__main__":
    controller = AutonomousController(model_path='model_steering_prediction.h5')
    try:
        controller.run()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Dừng chương trình...")
    finally:
        controller.stop()
