import math
import os
import csv
import time
import threading
from pyPS4Controller.controller import Controller
from main_func import AlphaBot 
import cv2

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None
class MyController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.bot = AlphaBot()  
        self.last_x = 0
        self.last_y = 0
        self.angle = 0
        self.speed = 0
        self.running = True
        self.camera_initialized = False
        self.images_folder = "captured_images"
        self.csv_filename = "image_log.csv"
        self.image_counter = 0

        if Picamera2:
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (480, 240)}))
            self.picam2.start()
            self.camera_initialized = True
        os.makedirs(self.images_folder, exist_ok=True)
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Image_Path", "Angle"])
    def capture_image(self):
        if self.camera_initialized:
            image_path = os.path.join(self.images_folder, f"image_{self.image_counter}.jpg")
            im = self.picam2.capture_array()
            cv2.imwrite(image_path, cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            print(f"Image captured and saved to {image_path}")
            self.image_counter += 1

            with open(self.csv_filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([image_path, self.angle])
    def update_direction(self):
        self.angle = math.atan2(self.last_y, self.last_x) * (180 / math.pi)
        self.angle /= 180
        if self.angle != 0:
            self.capture_image()
        print(self.angle)
        self.speed = math.sqrt(self.last_x**2 + self.last_y**2) / 32767 * 100
        self.speed = min(max(self.speed, 0), 100)
        if -0.5 < self.angle < 0.5:
            self.bot.left(self.speed)
        elif 0.94 <= self.angle <= 1 or -1 <= self.angle < -0.94:
            self.bot.right(self.speed)
        elif 0.055 < self.angle < 0.94:
            self.bot.forward(self.speed)
        elif -0.94 <= self.angle < -0.055:
            self.bot.backward(self.speed)
        else:
            self.bot.stop()
    def on_L3_up(self, value):
        self.last_y = -value
        self.update_direction()
    def on_L3_down(self, value):
        self.last_y = -value
        self.update_direction()

    def on_L3_left(self, value):
        self.last_x = -value
        self.update_direction()

    def on_L3_right(self, value):
        self.last_x = -value
        self.update_direction()

    def on_L3_x_at_rest(self):
        self.last_x = 0
        self.update_direction()

    def on_L3_y_at_rest(self):
        self.last_y = 0
        self.update_direction()

    def stop_capture(self):
        self.running = False
        self.bot.shutdown()
if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    try:
        controller.listen(timeout=60)
    finally:
        controller.stop_capture()