// Debug 
console.log("Made by Mbonu Chinedum")

// Getting the dom elements 
const emailAddress = document.getElementById("emailAddress"); 
const password = document.getElementById("password"); 
const loginBtn = document.getElementById("loginBtn"); 

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
        // 
        console.log(data); 
    })
})