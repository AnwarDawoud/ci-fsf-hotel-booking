document.addEventListener( 'DOMContentLoaded', function ()
{

    // Placeholder function for fetching user statistics
    async function fetchUserStatistics ()
    {
        // Replace the URL with your actual API endpoint for user statistics
        try
        {
            const response = await fetch( '/api/user_statistics/' );
            if ( !response.ok )
            {
                throw new Error( 'Network response was not ok' );
            }
            return await response.json();
        } catch ( error )
        {
            return console.error( 'Error fetching user statistics:', error );
        }
    }

    // Function to initialize user statistics chart
    function initializeUserStatisticsChart ()
    {
        var userData = {
            labels: [],
            datasets: [ {
                label: 'User Statistics',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(51, 204, 51, 0.5)',
                    'rgba(255, 153, 0, 0.5)',
                    'rgba(0, 102, 204, 0.5)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(51, 204, 51, 1)',
                    'rgba(255, 153, 0, 1)',
                    'rgba(0, 102, 204, 1)',
                ],
                borderWidth: 1
            } ]
        };

        var userStatisticsCanvas = document.getElementById( 'userStatisticsChart' );
        var userStatisticsChart;

        if ( userStatisticsCanvas && userStatisticsCanvas.getContext )
        {
            // Destroy existing chart instance if it exists
            var existingChart = Chart.getChart( userStatisticsCanvas );
            if ( existingChart )
            {
                existingChart.destroy();
            }

            userStatisticsChart = new Chart( userStatisticsCanvas.getContext( '2d' ), {
                type: 'bar',
                data: userData,
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            ticks: {
                                autoSkip: false,
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            } );
        }

        return userStatisticsChart;
    }

    // Placeholder functions for updating charts
    function updateUserTypesChart ( data, userStatisticsChart )
    {
        var totalBookings = data.total_bookings;
        var totalRevenue = data.total_revenue;
        var averageRating = data.average_rating;
        var totalHotels = data.total_hotels; // Include additional data
        var averageGuests = data.average_guests; // Include additional data
        var totalClients = data.total_clients; // Include additional data
        var totalManagers = data.total_managers; // Include additional data
        var occupiedRooms = data.occupied_rooms; // Include additional data
        var avgBookingDuration = data.avg_booking_duration; // Include additional data

        userStatisticsChart.data.labels = [ 'Total Bookings', 'Total Revenue', 'Average Rating', 'Total Hotels', 'Average Guests per Booking', 'Total Clients', 'Total Managers', 'Occupied Rooms', 'Average Booking Duration' ];
        userStatisticsChart.data.datasets[ 0 ].data = [ totalBookings, totalRevenue, averageRating, totalHotels, averageGuests, totalClients, totalManagers, occupiedRooms, avgBookingDuration ];

        userStatisticsChart.update();

        // Log additional data
        console.log( 'Total Hotels:', totalHotels );
        console.log( 'Average Guests per Booking:', averageGuests );
        console.log( 'Total Clients:', totalClients );
        console.log( 'Total Managers:', totalManagers );
        console.log( 'Occupied Rooms:', occupiedRooms );
        console.log( 'Average Booking Duration:', avgBookingDuration );
    }

    // Initial data fetching and chart initialization
    var userStatisticsChart = initializeUserStatisticsChart();

    fetchUserStatistics()
        .then( data =>
        {
            console.log( 'User Statistics Data:', data );
            updateUserTypesChart( data, userStatisticsChart );
        } )
        .catch( error => console.error( 'Error fetching user statistics:', error ) );

    // Check if the form with ID 'booking-form' exists before adding event listener
    var bookingForm = document.getElementById( 'booking-form' );

    if ( bookingForm )
    {
        bookingForm.addEventListener( 'submit', function ( event )
        {
            event.preventDefault();

            // Gather form data
            var formData = new FormData( bookingForm );

            // Perform AJAX call
            fetch( '/api/bookings/', {
                method: 'POST',
                body: formData,
            } )
                .then( response => response.json() )
                .then( data =>
                {
                    console.log( 'Booking successful:', data );
                    // You can update the UI or perform other actions based on the response
                } )
                .catch( error =>
                {
                    console.error( 'Error:', error );
                    // Handle errors, show an alert, or perform other actions
                } );
        } );
    }
} );
