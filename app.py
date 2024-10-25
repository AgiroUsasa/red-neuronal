from flask import Flask, request, jsonify, send_from_directory
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
    return send_from_directory('', 'red_neuronal.html')

@app.route('/detect', methods=['POST'])
def predict():
    if 'image' not in request.json:
        return jsonify({'error': 'No se proporcionó una imagen'}), 400
    
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Realizar la detección de objetos con YOLOv8
    results = model(image)
    detecciones = []

    # Extraer la información de las detecciones
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordenadas de la caja delimitadora
            confidence = box.conf[0]      # Confianza de la predicción
            class_id = int(box.cls[0])    # ID de clase

            class_names = [
                "Apple_lle", "AppleUSB_Mause", "Commodore64", "ContexCalculators", 
                "GeniusGM_6000", "IBM3348", "MSX_DPC-200", "PowerBook160", "CuboMirro"
            ]
            class_name = class_names[class_id] if class_id < len(class_names) else "Desconocido"

            detecciones.append({
                'class_name': class_name,
                'confidence': confidence.item(),
                'box': [x1.item(), y1.item(), x2.item(), y2.item()]
            })

    # Enviar una notificación si hay detecciones
    if detecciones:
        return jsonify({'detecciones': detecciones, 'message': 'Se ha detectado una imagen con éxito'})
    else:
        return jsonify({'detecciones': [], 'message': 'No se detectaron objetos'})

if __name__ == '__main__':
    app.run(debug=True)
