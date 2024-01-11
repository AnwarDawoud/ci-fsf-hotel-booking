// hotels_booking\hotel_your_choice\static\hotel_your_choice_js\main.js

document.addEventListener('DOMContentLoaded', function () {
    // Add an event listener to the form
    var bookingForm = document.getElementById('booking-form');

    if (bookingForm) {
        bookingForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Gather form data
            var formData = new FormData(bookingForm);

            // Perform AJAX call
            fetch('/api/bookings/', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Booking successful:', data);
                    // You can update the UI or perform other actions based on the response
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle errors, show an alert, or perform other actions
                });
        });
    }

    // Add more JavaScript functionality as needed
});

// You can include other JavaScript code based on your project's requirements
