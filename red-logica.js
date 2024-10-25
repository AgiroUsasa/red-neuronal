const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const notification = document.getElementById('notification');

// Acceder a la cámara
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        // Iniciar captura de imágenes cada segundo
        setInterval(captureImage, 1000);
    })
    .catch(err => {
        console.error("Error al acceder a la cámara: ", err);
        showNotification("No se pudo acceder a la cámara.");
    });

// Función para capturar la imagen y enviarla al servidor
function captureImage() {
    // Establecer el tamaño del canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Dibujar el video en el canvas
    context.drawImage(video, 0, 0);

    // Capturar la imagen como Data URL
    const dataURL = canvas.toDataURL('image/png');

    // Enviar la imagen al servidor
    sendImageToServer(dataURL);
}

// Función para enviar la imagen al servidor
function sendImageToServer(dataURL) {
    fetch('http://localhost:5000/predict', { // Asegúrate de que la URL sea correcta
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataURL }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        console.log('Detecciones del servidor:', data.detecciones);
        if (data.message) {
            showNotification(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Función para mostrar notificaciones en el frontend
function showNotification(message) {
    notification.textContent = message;
    notification.style.display = 'block';
}
