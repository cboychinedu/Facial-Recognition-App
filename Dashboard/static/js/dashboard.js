// Getting the DOM elements 
const startCameraBtn = document.getElementById('startCameraBtn'); 
const stopCameraBtn = document.getElementById("stopCameraBtn");
const video = document.getElementById('webcam'); 

let stream = null; // Store the stream globally

// Start the camera 
startCameraBtn.addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(mediaStream) {
            stream = mediaStream; // Store the stream
            video.srcObject = stream;
            video.style.display = 'block';
        })
        .catch(function(error) {
            console.error("Error accessing webcam:", error);
        });
});

// Stop the camera
stopCameraBtn.addEventListener('click', function() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop()); // Stop all tracks
        video.srcObject = null; // Remove the video source
        video.style.display = 'block';
    }
});
