// ** captures user date input and loads available time slots **
// ** listens for appointment submission **

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


const dateApptForm = document.querySelector('#calendar-input-form')

const createApptForm = document.querySelector("#create-appointment")


dateApptForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
    document.querySelector("#live-alert-location").innerHTML= ""

    console.log(document.querySelector("#calendar-input").value)
    const calendarInputs = {
        "date-input": document.querySelector("#calendar-input").value,
        "start-time-input": document.querySelector("#start-input").value,
        "end-time-input": document.querySelector("#end-input").value
    }
    console.log(calendarInputs)

    fetch('/get-time-windows', {
        method: 'POST',
        body: JSON.stringify(calendarInputs),
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "same-origin"
    })
        .then((response) => response.json())
        .then((responseTimeSlots) => {
            console.log(responseTimeSlots)
            if (responseTimeSlots.includes("empty")) {
                document.querySelector("#appt-options").innerHTML = "No appointments available"
            }
            else if (responseTimeSlots.includes("time-error")) {
                alert("Error: second time slot must be a time after the first", "danger")
            }
            else {
                const timeSlotsList = [];
                 for (const item of responseTimeSlots)   {
                    timeSlotsList.push(`<div class="button" > <input type="radio" name="appt-input" value=${item[0]}></input> <label for=${item[0]} id=${item[0]} value=${item[1]} class="btn btn-default" >${item[1]} </div>`)
                 }
                const timeSlots = timeSlotsList.join("")
                document.querySelector("#time-slots").innerHTML = "Available time slots:"
                document.querySelector("#appt-options").innerHTML =
                timeSlots
        }
            
        });
    })

createApptForm.addEventListener("submit", (evt) => {
    evt.preventDefault();
    document.querySelector("#live-alert-location").innerHTML= ""
    const apptTime = document.querySelector('input[name="appt-input"]:checked').value
    const apptTime12hr = document.getElementById(apptTime).innerText
    const dateInput = document.querySelector("#calendar-input").value
    // console.log(apptTime)
    // console.log(apptTime12hr)
    document.querySelector("#time-slots").innerHTML = ""

    const bookingInputs = {
    "appt-time" : apptTime,
    "appt-time-12hr" : apptTime12hr,
    "date-input" : dateInput
}
    fetch('/book-tasting', {
        method: 'POST',
        body: JSON.stringify(bookingInputs),
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "same-origin"
    })
        .then((response) => response.json())
        .then((responseBooking) => {
            if (responseBooking.includes("no-time")) {
                alert("ERROR: Please choose a time slot!", "warning")
            }
            else if (responseBooking.includes("no-date")) {
                alert("ERROR: Please choose a date first!", "warning")
            }
            else if (responseBooking.includes("user-error")) {
                alert("Error! Only allowed ONE scheduled tasting per day. Choose another date?", "danger")
            }
            else {
                alert(`Successfully booked your appointment for ${dateInput} at ${apptTime12hr}!`, "success")
            }
    
});
})