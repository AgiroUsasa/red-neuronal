const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const notification = document.getElementById('notification');
const loadingScreen = document.getElementById('loading-screen');
const MIN_LOADING_TIME = 4000; // 4 segundos
let rect = { x: 0, y: 0, width: 0, height: 0 }; // Inicializar las coordenadas del rectángulo

// Función para mostrar pantalla de carga
function showLoading() {
    loadingScreen.style.display = 'flex';
}

// Función para ocultar la pantalla de carga
function hideLoading() {
    loadingScreen.style.display = 'none';
    video.style.display = 'block';  // Mostrar el video cuando termine la carga
    canvas.style.display = 'block'; // Mostrar el canvas
}

// Función para acceder a la cámara
async function startCamera() {
    showLoading(); // Mostrar pantalla de carga
    await new Promise(resolve => setTimeout(resolve, 4000)); // Mantener la pantalla de carga visible por al menos 2 segundos

    try {
        // Solicitar acceso a la cámara
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Asegurarse de que el canvas tenga el mismo tamaño que el video
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            hideLoading(); // Ocultar pantalla de carga cuando el video esté listo
        };
    } catch (err) {
        console.error("Error al acceder a la cámara: ", err);
        hideLoading(); // Ocultar pantalla de carga en caso de error

        // Notificar al usuario que no se pudo acceder a la cámara
        notification.textContent = "No se pudo acceder a la cámara. Asegúrate de permitir el acceso.";
        notification.style.display = 'block';
        
        // Ocultar la notificación después de 3 segundos
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }
}

// Cuando toda la página ha cargado completamente, incluyendo todos los recursos
window.onload = () => {
    hideLoading();  // Ocultar pantalla de carga cuando todo esté listo
    startCamera();  // Iniciar la cámara después de cargar la página
};

// Función para dibujar el rectángulo en el canvas
function drawRect() {
    context.clearRect(0, 0, canvas.width, canvas.height); // Limpiar el canvas
    if (rect.width > 0 && rect.height > 0) { // Solo dibujar si hay un tamaño válido
        context.strokeStyle = 'red'; // Color del rectángulo
        context.lineWidth = 4; // Ancho del borde
        context.strokeRect(rect.x, rect.y, rect.width, rect.height); // Dibujar el rectángulo
    }
}

// Llama a la función captureImage cuando se toca cualquier parte del body
document.body.addEventListener('touchend', captureImage);
// Agregar el evento de clic para dispositivos no táctiless
document.addEventListener( 'click',captureImage);

// Agregar el evento de clic para dispositivos no táctiles
video.addEventListener( 'click',captureImage);


// Función para capturar la imagen al tocar el video
function captureImage() {

    // Notificar al usuario que se aingresado al image
    notification.textContent = " hola mundo";
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 2000); // Ocultar después de 2 segundos
    // Establecer el tamaño del canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Dibujar el video en el canvas
    context.drawImage(video, 0, 0);

    // Capturar solo la parte del rectángulo
    const imageData = context.getImageData(rect.x, rect.y, rect.width, rect.height);
    const captureCanvas = document.createElement('canvas');
    captureCanvas.width = rect.width;
    captureCanvas.height = rect.height;
    const captureContext = captureCanvas.getContext('2d');
    captureContext.putImageData(imageData, 0, 0);

    const dataURL = captureCanvas.toDataURL('image/png');
    console.log(dataURL); // Aquí podrías enviar esta imagen al servidor para su procesamiento

    // Llamar a la función de predicción
    sendImageToServer(dataURL);
}

// Función para enviar la imagen al servidor
function sendImageToServer(dataURL) {
    fetch('https://github.com/AgiroUsasa/red-neuronal/blob/main/app.py', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataURL }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Detecciones del servidor:', data.detecciones);
        updateRectangle(data.detecciones); // Actualizar el rectángulo con las detecciones
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Función para actualizar el rectángulo con las coordenadas del objeto detectado
function updateRectangle(detecciones) {
    if (detecciones.length > 0) {
        // Suponiendo que las detecciones devuelven un array de objetos con las propiedades x, y, width, height
        const { x, y, width, height } = detecciones[0]; // Tomar la primera detección
        rect.x = x;
        rect.y = y;
        rect.width = width;
        rect.height = height;
    } else {
        // Limpiar el rectángulo si no hay detecciones
        rect.width = 0;
        rect.height = 0;
    }
}

// Dibujar el rectángulo cada vez que se actualiza el video
video.addEventListener('loadedmetadata', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
});

// Actualizar el rectángulo al redibujar en el video
video.addEventListener('play', () => {
    const update = () => {
        if (!video.paused && !video.ended) {
            drawRect(); // Redibujar el rectángulo en cada frame
            requestAnimationFrame(update);
        }
    };
    requestAnimationFrame(update);
});

// Iniciar la cámara al cargar la página
startCamera();
