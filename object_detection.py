# model/object_detection.py

import keras
import keras_hub
import cv2
import numpy as np

# Cargar el modelo
def load_model():
    model = keras_hub.load('https://tfhub.dev/some_yolov8_model_url')  # Cambia esto por la URL real del modelo
    return model

# Preprocesar la imagen
def preprocess(image):
    # Redimensionar y normalizar la imagen según las necesidades del modelo
    image = cv2.resize(image, (640, 640))  # Asegúrate de que el tamaño sea el correcto
    image = image / 255.0  # Normalizar
    return np.expand_dims(image, axis=0)  # Añadir una dimensión para el batch

# Hacer predicciones
def predict(image, model):
    preprocessed_image = preprocess(image)
    detections = model.predict(preprocessed_image)
    return detections
