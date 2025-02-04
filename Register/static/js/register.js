// Debug 
console.log("Made by Mbonu Chinedum")

// Getting the dom elements 
const firstname = document.getElementById("firstname"); 
const lastname = document.getElementById("lastname"); 
const emailAddress = document.getElementById("emailAddress"); 
const password = document.getElementById("password"); 
const registerBtn = document.getElementById("registerBtn"); 

// Setting an event listener for the register button 
registerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    
    // Getting the user's registeration data 
    let data = JSON.stringify({
        firstname: firstname.value, 
        lastname: lastname.value, 
        emailAddress: emailAddress.value, 
        password: password.value,
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
    const url = "/register/"; 

    // Making the fetch request to the backend server 
    $.ajax({
        // Setting the ajax configuration 
        type: 'POST', 
        url: url, 
        dataType: 'json', 
        contentType: 'application/json', 
        data: data,
        headers: headers,  
        crossDomain: true, 
    }).done((data) => {
        // 
        console.log(data); 
    })

    
})