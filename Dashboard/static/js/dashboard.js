let videoStream = null;

document.getElementById('startCameraBtn').addEventListener('click', function() {
    const video = document.getElementById('webcam');
    const img = document.getElementById('processedVideo');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
            video.style.display = 'block';
            img.style.display = 'block';
            videoStream = stream;
            processVideo();
        })
        .catch(function(error) {
            console.error("Error accessing webcam:", error);
        });
});

document.getElementById('stopCameraBtn').addEventListener('click', function() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        document.getElementById('webcam').srcObject = null;
        document.getElementById('processedVideo').style.display = 'none';
    }
});

function processVideo() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const img = document.getElementById('processedVideo');

    function captureFrame() {
        if (!videoStream) return;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const frame = canvas.toDataURL('image/jpeg');

        fetch('/dashboard/processFrame', {
            method: 'POST',
            body: JSON.stringify({ image: frame }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.processedImage) img.src = data.processedImage;
            setTimeout(captureFrame, 100);
        })
        .catch(error => console.error("Error processing frame:", error));
    }

    captureFrame();
}

window.addEventListener('beforeunload', function() {
    if (videoStream) videoStream.getTracks().forEach(track => track.stop());
});
