// Getting the dom elements 
const fileBtn = document.getElementById("file"); 
const selectImageBtn = document.getElementById("selectImageBtn"); 
const uploadImageBtn = document.getElementById("uploadImageBtn"); 
const startCameraBtn = document.getElementById('startCameraBtn'); 
const stopCameraBtn = document.getElementById('stopCameraBtn'); 
const imageAnalysis = document.getElementById("imageAnalysis"); 

// Setting the video stream as null 
let videoStream = null;

// Adding event listener for the select image buttons 
selectImageBtn.addEventListener("click", (event) => {
    fileBtn.click(); 
})

// Setting event listener for the upload button 
uploadImageBtn.addEventListener("click", (event) => {
    // Execute this block of code below if the upload image button 
    // was clicked 
    const file = fileBtn.files[0]; 
    let formData = new FormData(); 

    // Appending the file into the form data before sending it back 
    // to the server 
    formData.append('image', file); 

    // Using fetch request 
    fetch('/dashboard/processImage', {
        method: 'POST', 
        body: formData
    })
    .then(response => response.json())
    .then((data) => {
        // if the processed image is present 
        if (data.processedImage) {
            imageAnalysis.src = data.processedImage; 
        }
    })
})

// Adding event listener for the start camera button 
startCameraBtn.addEventListener('click', function() {

    // Getting the dom elements 
    const video = document.getElementById('webcam');
    const img = document.getElementById('processedVideo');

    // Starting the video 
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

// Setting an event listener for stoping the camera
stopCameraBtn.addEventListener('click', function() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        document.getElementById('webcam').srcObject = null;
        document.getElementById('processedVideo').style.display = 'none';
    }
});

// Creating a function for processing the video 
const processVideo = () => {
    // Getting the webcam, canvas and processed video dom elements 
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const img = document.getElementById('processedVideo');

    // Creating a function called capture frame for capturing 
    // the web frames
    const captureFrame = () => {
        // if there is no video 
        if (!videoStream) return;

        // Get the video width and height
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // draw the image, and convert it into a dataurl image 
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const frame = canvas.toDataURL('image/jpeg');

        // Send the image to the backend for further preprocessing 
        fetch('/dashboard/processFrame', {
            method: 'POST',
            body: JSON.stringify({ image: frame }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            // if the response has the preprocessed image, display the image 
            // inside the img tag
            if (data.processedImage) img.src = data.processedImage;
            setTimeout(captureFrame, 100);
        })
        .catch(error => console.error("Error processing frame:", error));
    }

    // Start the function capture frame 
    captureFrame();
}

// 
window.addEventListener('beforeunload', function() {
    if (videoStream) videoStream.getTracks().forEach(track => track.stop());
});
