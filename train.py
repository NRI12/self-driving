import os
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Lambda
from imgaug import augmenters as iaa
df = pd.read_csv('image_log.csv', header=None, names=['Image_Path', 'Steering'])

images = []  
steerings = []
#Augement and process
def preProcess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)  
    img = cv2.resize(img, (200, 66)) 
    img = img / 255 
    return img
def augmentImage(imgPath, steering):
    img = mpimg.imread(imgPath)
    # Dịch chuyển ngẫu nhiên
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        img = pan.augment_image(img)
    # Phóng to ngẫu nhiên
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    # Thay đổi độ sáng ngẫu nhiên
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.5, 1.2))
        img = brightness.augment_image(img)
    # Lật ảnh và giá trị điều khiển nếu ngẫu nhiên quyết định
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        steering = -steering
    return img, steering
for img_path, steering in zip(df['Image_Path'], df['Steering']):
    img, steering = augmentImage(img_path, steering)
    img = preProcess(img)
    images.append(img)
    steerings.append(steering)
images = np.array(images)
steerings = np.array(steerings)
print(images.shape)
print(steerings.shape)
#build network
def build_model():
    model = Sequential([
        Lambda(lambda x: x / 0.5 - 1.0, input_shape=(66, 200, 3)), 
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Dropout(0.5),
        Flatten(),
        Dense(100, activation='relu'),
        Dense(50, activation='relu'),
        Dense(10, activation='relu'),
        Dense(1)
    ])
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(images, steerings, test_size=0.2, random_state=0)
model = build_model()
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val), batch_size=10, verbose=1)
# Đánh giá mô hình
evaluation = model.evaluate(X_val, y_val)
print(f"Loss trên tập kiểm thử: {evaluation}")
# Lưu mô hình
model.save('model_steering_prediction.h5')
