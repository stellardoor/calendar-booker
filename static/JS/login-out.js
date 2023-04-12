'use strict';

const alert = (message, type) => {
    const alertLocation = document.getElementById("live-alert-location")
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
  
    alertLocation.append(wrapper)
  }


const loginForm = document.querySelector('#login-form')


loginForm.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        "email" : document.querySelector("#email").value, 
        "password" : document.querySelector("#password").value
    };

    console.log(formInputs)

    fetch('/process-login', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "same-origin"
    })
        .then((response) => response.text())
        .then((responseAccount) => {
            console.log(responseAccount)
            if (responseAccount === "success") {
                alert("success")
                window.location.href="/"
            }
            else {
                document.querySelector("#password").value = ""
                alert("Error: Password or Email incorrect", "danger")
            }
        })
            
        })