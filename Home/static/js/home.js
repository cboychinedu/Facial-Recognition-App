// Debug 
console.log("Made by Mbonu Chinedum")

// Getting the dom elements 
const emailAddress = document.getElementById("emailAddress"); 
const password = document.getElementById("password"); 
const loginBtn = document.getElementById("loginBtn"); 
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const mobileMenu = document.getElementById('mobile-menu');

menuBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('-translate-x-full');
    mobileMenu.classList.add('translate-x-0');
});

closeBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('translate-x-0');
    mobileMenu.classList.add('-translate-x-full');
});

// Setting an event listener for the login button 
loginBtn.addEventListener("click", (event) => {
    // prevent default submission 
    event.preventDefault(); 

    // Getting the user's registeration data 
    let data = JSON.stringify({
        emailAddress: emailAddress.value, 
        password: password.value
    })

    /**
     * Setting the request header, the http verbs, 
     * and the URL for the register route 
    */
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    // Setting the url 
    const url = "/"; 

    // Making the fetch request to the backend server 
    $.ajax({
        // Setting the ajax configurations 
        type: "POST", 
        url: url, 
        dataType: 'json', 
        contentType: 'application/json', 
        data: data, 
        headers: headers, 
        crossDomain: true, 
    })
    .done((data) => {
        // if the status message is success 
        if (data["status"] === "success") {
            setInterval(() => {
                // redirect the user to the dashboard 
                location.href = '/dashboard'
            }, 1000)
        } 

        // Else if the status returned an error code 
        else if (data.status ===  "error") {
            // Execute the block of code below if the returned status code 
            // was an error 
            alert(data.message); 

            // closing up 
            return; 
        }
    })
})