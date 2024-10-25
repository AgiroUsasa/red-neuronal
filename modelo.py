from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='dataset.yaml', epochs=50)

# El modelo debería guardarse automáticamente en la ruta predeterminada
