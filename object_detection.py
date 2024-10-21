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

    # Procesar las detecciones
    return process_detections(detections)

def process_detections(detections):
    results = []
    # Asumiendo que detections es un tensor con la forma [batch_size, num_detections, 6]
    # donde las columnas son [x_min, y_min, x_max, y_max, class_id, score]
    for detection in detections[0]:  # Iterar sobre la primera (y única) imagen en el batch
        x_min, y_min, x_max, y_max, class_id, score = detection

        # Filtrar detecciones con baja puntuación
        if score >= 0.5:  # Ajusta este umbral según sea necesario
            results.append({
                'class': int(class_id),
                'x': int(x_min),
                'y': int(y_min),
                'width': int(x_max - x_min),
                'height': int(y_max - y_min)
            })

    return results
