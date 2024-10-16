// script.js

const video = document.getElementById('video');

// Acceder a la cámara y reproducir el video
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error al acceder a la cámara: ", err);
    }
}

// Capturar imagen
document.getElementById('capture').addEventListener('click', () => {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    const dataURL = canvas.toDataURL('image/png');
    console.log(dataURL); // Aquí podrías enviar esta imagen al servidor para su procesamiento

    // Llamar a la función de predicción
    sendImageToServer(dataURL);
});

// Función para enviar la imagen al servidor
function sendImageToServer(dataURL) {
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataURL }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Iniciar la cámara al cargar la página
startCamera();
