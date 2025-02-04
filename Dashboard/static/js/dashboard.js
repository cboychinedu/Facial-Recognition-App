// Getting the dom elements 
const startCameraBtn = document.getElementById('startCameraBtn'); 


// 
startCameraBtn.addEventListener('click', function() {
    const video = document.getElementById('webcam');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
            video.style.display = 'block';
        })
        .catch(function(error) {
            console.error("Error accessing webcam:", error);
        });
});