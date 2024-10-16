from flask import Flask, request, jsonify
import os
import base64
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)

# Cargar el modelo YOLOv8
model = YOLO('yolov8.pt')  # Cambia 'yolov8.pt' por el modelo que estás utilizando

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']
    # Decodificar la imagen
    img_data = base64.b64decode(data.split(',')[1])
    
    # Guardar la imagen temporalmente para procesamiento
    img_path = 'img/temp_image.jpg'
    with open(img_path, 'wb') as f:
        f.write(img_data)
    
    # Procesar la imagen usando OpenCV
    image = cv2.imread(img_path)
    
    # Realizar la detección de objetos con YOLOv8
    results = model(image)

    # Extraer información de la detección
    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordenadas de la caja delimitadora
            confidence = box.conf[0]      # Confianza de la predicción
            class_id = int(box.cls[0])    # ID de clase
            detections.append({
                'class_id': class_id,
                'confidence': confidence.item(),
                'box': [x1.item(), y1.item(), x2.item(), y2.item()]
            })

    # Eliminar la imagen temporal si no es necesaria
    os.remove(img_path)

    return jsonify({'detecciones': detections})

if __name__ == '__main__':
    app.run(debug=True)
