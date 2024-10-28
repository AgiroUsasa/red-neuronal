from flask import Flask, request, jsonify, send_from_directory
import os
import base64
import numpy as np
import cv2
from ultralytics import YOLO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el modelo YOLOv8
try:
    model = YOLO('detect.v1i.yolov8/dataset.txt')  # Ruta a tu modelo entrenado
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# Definir los colores esperados para cada objeto
colores_esperados = {
    "Apple_lle": ((35, 100, 100), (85, 255, 255)),  # Ejemplo de color verde
    "AppleUSB_Mause": ((0, 100, 100), (10, 255, 255)),  # Rojo
    "Commodore64": ((100, 100, 100), (140, 255, 255)),  # Azul
    "ContexCalculators": ((0, 0, 0), (180, 255, 30)),  # Negro
    "GeniusGM_6000": ((0, 100, 100), (10, 255, 255)),  # Rojo
    "IBM3348": ((0, 0, 200), (180, 25, 255)),  # Gris oscuro
    "MSX_DPC-200": ((20, 100, 100), (30, 255, 255)),  # Amarillo
    "PowerBook160": ((100, 150, 0), (140, 255, 255)),  # Verde oscuro
    "CuboMirro": [  # Definir dos rangos para "CuboMirro"
        ((20, 100, 100), (30, 255, 255)),  # Dorado
        ((0, 0, 0), (180, 255, 30))        # Negro
    ],
}

def detectar_color(imagen, caja, class_name):
    # Extraer la región del objeto detectado
    x1, y1, x2, y2 = caja
    objeto_roi = imagen[int(y1):int(y2), int(x1):int(x2)]

    # Convertir a espacio de color HSV
    hsv = cv2.cvtColor(objeto_roi, cv2.COLOR_BGR2HSV)

    # Obtener los rangos de color esperados
    rango_color = colores_esperados.get(class_name, None)

    if rango_color:
        if isinstance(rango_color[0], tuple):
            # Un solo rango
            mascara = cv2.inRange(hsv, np.array(rango_color[0]), np.array(rango_color[1]))
            porcentaje = cv2.countNonZero(mascara) / (objeto_roi.shape[0] * objeto_roi.shape[1]) * 100
            return porcentaje > 10, porcentaje
        else:
            # Múltiples rangos
            for rango in rango_color:
                mascara = cv2.inRange(hsv, np.array(rango[0]), np.array(rango[1]))
                porcentaje = cv2.countNonZero(mascara) / (objeto_roi.shape[0] * objeto_roi.shape[1]) * 100
                if porcentaje > 10:
                    return True, porcentaje

    return False, 0

@app.route('/')
def index():
    return send_from_directory('', 'red_neuronal.html')

@app.route('/predict', methods=['POST'])
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

            # Detectar el color del objeto
            color_detectado, porcentaje_color = detectar_color(image, (x1.item(), y1.item(), x2.item(), y2.item()), class_name)

            detecciones.append({
                'class_name': class_name,
                'confidence': confidence.item(),
                'box': [x1.item(), y1.item(), x2.item(), y2.item()],
                'color_detectado': color_detectado,  # Resultado de la detección de color
                'porcentaje_color': porcentaje_color  # Porcentaje del color detectado
            })

    # Enviar una notificación si hay detecciones
    if detecciones:
        return jsonify({'detecciones': detecciones, 'message': 'Se ha detectado una imagen con éxito'})
    else:
        return jsonify({'detecciones': [], 'message': 'No se detectaron objetos'})

if __name__ == '__main__':
    app.run(debug=True)
