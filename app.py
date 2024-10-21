# server/app.py

from flask import Flask, request, jsonify
import cv2
import os
import base64
from object_detection import load_model, predict

app = Flask(__name__)
model = load_model()

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    image_data = data['image'].split(',')[1]  # Eliminar la parte de Data URL
    image = decode_image(image_data)
    
    detections = predict(image, model)  # Llama a tu función de predicción
    return jsonify({'detecciones': detections})

def decode_image(data):
    # Decodificar la imagen desde base64
    img_data = base64.b64decode(data)
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def predict_object():
    data = request.json['image']
    # Decodificar la imagen
    img_data = base64.b64decode(data.split(',')[1])
    
    # Guardar la imagen temporalmente para procesamiento
    img_path = 'img/temp_image.jpg'
    with open(img_path, 'wb') as f:
        f.write(img_data)
    
    # Procesar la imagen usando OpenCV
    image = cv2.imread(img_path)

    # Realizar la detección de objetos
    detections = predict(image, model)  # Usa la función de predicción

    # Procesar las detecciones y preparar la respuesta
    detecciones_formateadas = process_detections(detections)

    # Eliminar la imagen temporal si no es necesaria
    os.remove(img_path)

    return jsonify({'detecciones': detecciones_formateadas})

def process_detections(detections):
    # Procesar las detecciones del modelo y devolver una lista de resultados
    results = []
    for detection in detections:
        # Ajusta el procesamiento según la salida de tu modelo
        results.append({
            'class': detection['class'],  # Cambia esto según tu salida
            'x': int(detection['x']),
            'y': int(detection['y']),
            'width': int(detection['width']),
            'height': int(detection['height'])
        })
    return results

if __name__ == '__main__':
    app.run(debug=True)
