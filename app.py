# server/app.py

from flask import Flask, request, jsonify
import os
import base64
import numpy as np
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Cargar el modelo YOLOv8
model = YOLO('detect.v1i.yolov8/test.pt')  # Ruta a tu modelo entrenado
@app.route('/')
def index():
    return send_from_directory('red_neuronal.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.json:
        return jsonify({'error': 'No image provided'}), 400
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
    detecciones = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordenadas de la caja delimitadora
            confidence = box.conf[0]      # Confianza de la predicción
            class_id = int(box.cls[0])    # ID de clase

            # Aquí puedes mapear class_id a tus nombres de clase
            class_names = [
                "Apple_lle",
                "AppleUSB_Mause",
                "Commodore64",
                "ContexCalculators",
                "GeniusGM_6000",
                "IBM3348",
                "MSX_DPC-200",
                "PowerBook160"
                "CuboMirro"
            ]
            class_name = class_names[class_id] if class_id < len(class_names) else "Unknown"

            detecciones.append({
                'class_name': class_name,  # Cambié class_id a class_name
                'confidence': confidence.item(),
                'box': [x1.item(), y1.item(), x2.item(), y2.item()]
            })

    # Eliminar la imagen temporal si no es necesaria
    os.remove(img_path)

    return jsonify({'detecciones': detecciones})

if __name__ == '__main__':
    app.run(debug=True)
