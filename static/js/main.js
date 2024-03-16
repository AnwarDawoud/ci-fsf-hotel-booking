// document.addEventListener( 'DOMContentLoaded', function ()
// {

//     // Placeholder function for fetching user statistics
//     async function fetchUserStatistics ()
//     {
//         // Replace the URL with your actual API endpoint for user statistics
//         try
//         {
//             const response = await fetch( '/api/user_statistics/' );
//             if ( !response.ok )
//             {
//                 throw new Error( 'Network response was not ok' );
//             }
//             return await response.json();
//         } catch ( error )
//         {
//             return console.error( 'Error fetching user statistics:', error );
//         }
//     }

// // Function to initialize user statistics chart
// function initializeUserStatisticsChart ()
// {
//     var userData = {
//         labels: [],
//         datasets: [ {
//             label: 'User Statistics',
//             data: [],
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.5)',
//                 'rgba(54, 162, 235, 0.5)',
//                 'rgba(255, 206, 86, 0.5)',
//                 'rgba(75, 192, 192, 0.5)',
//                 'rgba(153, 102, 255, 0.5)',
//                 'rgba(255, 159, 64, 0.5)',
//                 'rgba(51, 204, 51, 0.5)',
//                 'rgba(255, 153, 0, 0.5)',
//                 'rgba(0, 102, 204, 0.5)',
//             ],
//             borderColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)',
//                 'rgba(51, 204, 51, 1)',
//                 'rgba(255, 153, 0, 1)',
//                 'rgba(0, 102, 204, 1)',
//             ],
//             borderWidth: 1
//         } ]
//     };

//     var userStatisticsCanvas = document.getElementById( 'userStatisticsChart' );
//     var userStatisticsChart;

//     if ( userStatisticsCanvas && userStatisticsCanvas.getContext )
//     {
//         // Destroy existing chart instance if it exists
//         var existingChart = Chart.getChart( userStatisticsCanvas );
//         if ( existingChart )
//         {
//             existingChart.destroy();
//         }

//         userStatisticsChart = new Chart( userStatisticsCanvas.getContext( '2d' ), {
//             type: 'bar',
//             data: userData,
//             options: {
//                 responsive: true,
//                 scales: {
//                     x: {
//                         ticks: {
//                             autoSkip: false,
//                         }
//                     },
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         } );
//     }

//     return userStatisticsChart;
// }

// Placeholder functions for updating charts
// function updateUserTypesChart ( data, userStatisticsChart )
// {
//     var totalBookings = data.total_bookings;
//     var totalRevenue = data.total_revenue;
//     var averageRating = data.average_rating;
//     var totalHotels = data.total_hotels; // Include additional data
//     var averageGuests = data.average_guests; // Include additional data
//     var totalClients = data.total_clients; // Include additional data
//     var totalManagers = data.total_managers; // Include additional data
//     var occupiedRooms = data.occupied_rooms; // Include additional data
//     var avgBookingDuration = data.avg_booking_duration; // Include additional data

//     userStatisticsChart.data.labels = [ 'Total Bookings', 'Total Revenue', 'Average Rating', 'Total Hotels', 'Average Guests per Booking', 'Total Clients', 'Total Managers', 'Occupied Rooms', 'Average Booking Duration' ];
//     userStatisticsChart.data.datasets[ 0 ].data = [ totalBookings, totalRevenue, averageRating, totalHotels, averageGuests, totalClients, totalManagers, occupiedRooms, avgBookingDuration ];

//     userStatisticsChart.update();

//     // Log additional data
//     console.log( 'Total Hotels:', totalHotels );
//     console.log( 'Average Guests per Booking:', averageGuests );
//     console.log( 'Total Clients:', totalClients );
//     console.log( 'Total Managers:', totalManagers );
//     console.log( 'Occupied Rooms:', occupiedRooms );
//     console.log( 'Average Booking Duration:', avgBookingDuration );
// }

// // Initial data fetching and chart initialization
// var userStatisticsChart = initializeUserStatisticsChart();

//     fetchUserStatistics()
//         .then( data =>
//         {
//             console.log( 'User Statistics Data:', data );
//             updateUserTypesChart( data, userStatisticsChart );
//         } )
//         .catch( error => console.error( 'Error fetching user statistics:', error ) );

//     // Check if the form with ID 'booking-form' exists before adding event listener
//     var bookingForm = document.getElementById( 'booking-form' );

//     if ( bookingForm )
//     {
//         bookingForm.addEventListener( 'submit', function ( event )
//         {
//             event.preventDefault();

//             // Gather form data
//             var formData = new FormData( bookingForm );

//             // Perform AJAX call
//             fetch( '/api/bookings/', {
//                 method: 'POST',
//                 body: formData,
//             } )
//                 .then( response => response.json() )
//                 .then( data =>
//                 {
//                     console.log( 'Booking successful:', data );
//                     // You can update the UI or perform other actions based on the response
//                 } )
//                 .catch( error =>
//                 {
//                     console.error( 'Error:', error );
//                     // Handle errors, show an alert, or perform other actions
//                 } );
//         } );
//     }
// } );

// hotel_script.js

// Function to show read more modal
function showReadMoreModal ( hotelId )
{
    $( `#readMoreModal${ hotelId }` ).show();
}

// Function to hide read more modal
function hideReadMoreModal ( hotelId )
{
    $( `#readMoreModal${ hotelId }` ).hide();
}

// Function to toggle other photos
function toggleOtherPhotos ( hotelId )
{
    const otherPhotosContainer = document.getElementById( `otherPhotos${ hotelId }` );
    const showPhotosButton = document.getElementById( `showPhotosButton${ hotelId }` );

    if ( otherPhotosContainer && showPhotosButton )
    {
        otherPhotosContainer.style.display = otherPhotosContainer.style.display === 'none' ? 'block' : 'none';
        showPhotosButton.innerText = otherPhotosContainer.style.display === 'none' ? 'Show All Photos' : 'Hide Photos';
    } else
    {
        console.error( 'Elements not found. Check if the IDs are correct.' );
    }
}

// Declare variables
let isEnlargedVisible = false;
let currentHotelId; // Assuming this is declared somewhere else in your code.

// Function to debounce
function debounce ( func, delay )
{
    let inDebounce;
    return function ()
    {
        const context = this;
        const args = arguments;
        clearTimeout( inDebounce );
        inDebounce = setTimeout( () => func.apply( context, args ), delay );
    };
}

// Function to show enlarged image
function showEnlarged ( imageSrc, hotelId )
{
    const enlargedContainer = document.getElementById( 'enlargedContainer' );
    const enlargedImage = document.getElementById( 'enlargedImage' );
    const allImages = Array.from( document.querySelectorAll( `.hotel-photos img[data-hotel-id="${ hotelId }"], .other-photos img[data-hotel-id="${ hotelId }"]` ) );

    // Set image source and display container
    enlargedImage.src = imageSrc;
    enlargedContainer.style.display = 'flex';
    currentHotelId = hotelId;

    // Function to hide enlarged image
    function hideEnlarged ()
    {
        enlargedContainer.style.display = 'none';
        isEnlargedVisible = false;
        document.getElementById( 'leftArrow' ).removeEventListener( 'click', showPreviousImage );
        document.getElementById( 'rightArrow' ).removeEventListener( 'click', showNextImage );
    }

    // Toggle visibility of enlarged image
    enlargedContainer.onclick = hideEnlarged;
    isEnlargedVisible = true;

    // Function to show next image
    function showNextImage ()
    {
        const currentIndex = allImages.findIndex( img => img.src === enlargedImage.src );
        const nextIndex = ( currentIndex + 1 ) % allImages.length;
        if ( allImages[ nextIndex ] )
        {
            enlargedImage.src = allImages[ nextIndex ].src;
        }
    }

    // Function to show previous image
    function showPreviousImage ()
    {
        const currentIndex = allImages.findIndex( img => img.src === enlargedImage.src );
        const previousIndex = ( currentIndex - 1 + allImages.length ) % allImages.length;
        if ( allImages[ previousIndex ] )
        {
            enlargedImage.src = allImages[ previousIndex ].src;
        }
    }

    // Add click event listeners to arrows
    document.getElementById( 'leftArrow' ).onclick = event =>
    {
        event.stopPropagation();
        showPreviousImage();
    };

    document.getElementById( 'rightArrow' ).onclick = event =>
    {
        event.stopPropagation();
        showNextImage();
    };
}

// Add click event listener to all images
const allImages = document.querySelectorAll( '.hotel-photos img, .other-photos img' );
allImages.forEach( image =>
{
    image.addEventListener( 'click', function ()
    {
        const imageSrc = this.src;
        const hotelId = this.getAttribute( 'data-hotel-id' );
        showEnlarged( imageSrc, hotelId );
    } );
} );


// Function to handle like and dislike actions
function handleLikeDislike ( form, url )
{
    $.ajax( {
        type: 'POST',
        url: url,
        data: form.serialize(),
        success: function ( response )
        {
            console.log( 'Success:', response );

            // Update the like or dislike count on the page
            var commentId = form.data( 'comment-id' );
            var likeCountElement = form.closest( '.comment' ).find( '.like-count' );
            var dislikeCountElement = form.closest( '.comment' ).find( '.dislike-count' );

            likeCountElement.text( response.likes_count );
            dislikeCountElement.text( response.dislikes_count );

            // Disable the like/dislike buttons after a successful click
            form.find( '.like-comment-btn, .dislike-comment-btn' ).prop( 'disabled', true );

            // Prevent the default form submission
            return false;
        },
        error: function ( error )
        {
            console.log( 'Error:', error );
        },
    } );
}

// Function to handle adding a new comment
function handleAddComment ( form, url )
{
    $.ajax( {
        type: 'POST',
        url: url,
        data: form.serialize(),
        success: function ( response )
        {
            console.log( 'Success:', response );

            // Check if the status is success and the comment_id exists
            if ( response.status === 'success' && response.comment_id )
            {
                // Create a new comment element and append it to the comments container
                var newComment = '<li class="comment" data-comment-id="' + response.comment_id + '">' +
                    '<p>' + response.comment_text + '</p>' +
                    '<div class="like-dislike">' +
                    '<button type="button" class="like-comment-btn" data-like-url="' + url + '" data-comment-id="' + response.comment_id + '">👍<span class="like-count">0</span></button>' +
                    '<button type="button" class="dislike-comment-btn" data-dislike-url="' + url + '" data-comment-id="' + response.comment_id + '">👎<span class="dislike-count">0</span></button>' +
                    '</div>' +
                    '</li>';

                // Append the new comment to the comments container
                $( '.comment-list' ).append( newComment );

                // Clear the comment input field
                form.find( '#id_text' ).val( '' );
            }
        },
        error: function ( error )
        {
            console.log( 'Error:', error );
        },
    } );
}

// Submit the like form
$( document ).on( 'submit', '.like-form', function ( event )
{
    event.preventDefault();
    var form = $( this );
    var url = form.attr( 'action' );
    handleLikeDislike( form, url );
} );

// Submit the dislike form
$( document ).on( 'submit', '.dislike-form', function ( event )
{
    event.preventDefault();
    var form = $( this );
    var url = form.attr( 'action' );
    handleLikeDislike( form, url );
} );

// Submit the add comment form
$( document ).on( 'submit', '.add-comment-form', function ( event )
{
    event.preventDefault();
    var form = $( this );
    var url = form.attr( 'action' );
    handleAddComment( form, url );
} );

// Function to get CSRF token from cookies
function getCookie ( name )
{
    const cookieString = document.cookie;
    const cookies = cookieString.split( '; ' );

    for ( let i = 0; cookies.length; i++ )
    {
        const cookie = cookies[ i ].split( '=' );
        if ( cookie[ 0 ] === name )
        {
            return cookie[ 1 ];
        }
    }

    return null;
}

// Function to delete comment
function deleteComment ( commentId, csrfToken )
{
    console.log( 'Deleting comment with ID:', commentId );
    console.log( 'CSRF Token:', csrfToken );

    console.log( 'Initiating deleteComment fetch request...' );

    fetch( `/delete_comment/${ commentId }/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    } )
        .then( response =>
        {
            console.log( 'Response:', response );

            if ( !response.ok )
            {
                throw new Error( `HTTP error! Status: ${ response.status }` );
            }

            return response.json();
        } )
        .then( data =>
        {
            console.log( 'Server data:', data );

            if ( data.success )
            {
                const commentElement = document.querySelector( `.comment[data-comment-id="${ commentId }"]` );
                commentElement.remove();
            } else
            {
                console.error( 'Comment deletion failed.' );
            }
        } )
        .catch( error =>
        {
            console.error( 'Error during comment deletion:', error );
        } );
}

// Event listener to delete comment
document.getElementById( 'hotelContainer' ).addEventListener( 'click', function ( event )
{
    if ( event.target.classList.contains( 'deleteCommentButton' ) )
    {
        var commentId = event.target.getAttribute( 'data-comment-id' );

        // Fetch CSRF token
        var csrfToken = getCookie( 'csrftoken' );

        // Check if the CSRF token is available
        if ( !csrfToken )
        {
            console.error( 'CSRF token not available.' );
            return;
        }

        console.log( 'CSRF Token:', csrfToken );

        // Pass CSRF token to deleteComment function
        deleteComment( commentId, csrfToken );
    }
} );

// Initialize modals
document.addEventListener( 'DOMContentLoaded', function ()
{
    var elems = document.querySelectorAll( '.modal' );
    var instances = M.Modal.init( elems );
} );


document.addEventListener( 'DOMContentLoaded', function ()
{
    // Placeholder function for fetching user data
    function fetchUserData ()
    {
        // Replace the URL with your actual API endpoint for user data
        return fetch( '/api/user_data/' )
            .then( response =>
            {
                if ( !response.ok )
                {
                    throw new Error( 'Network response was not ok' );
                }
                return response.json();
            } )
            .catch( error => console.error( 'Error fetching user data:', error ) );
    }

    // Function to initialize user table
    function initializeUserTable ( userData )
    {
        // Your logic to initialize the user table based on the retrieved data
        console.log( 'User Data:', userData );
    }

    // Placeholder function for updating user permissions
    function updatePermissions ( userId, newPermissions )
    {
        // Perform an API request to update user permissions
        fetch( `/api/update_permissions/${ userId }`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify( { permissions: newPermissions } ),
        } )
            .then( response => response.json() )
            .then( data =>
            {
                console.log( 'Permissions updated successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error =>
            {
                console.error( 'Error updating permissions:', error );
                // Handle errors, show an alert, or perform other actions
            } );
    }

    // Placeholder function for deleting a user
    function deleteUser ( userId )
    {
        // Perform an API request to delete the user
        fetch( `/api/delete_user/${ userId }`, {
            method: 'DELETE',
        } )
            .then( response => response.json() )
            .then( data =>
            {
                console.log( 'User deleted successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error =>
            {
                console.error( 'Error deleting user:', error );
                // Handle errors, show an alert, or perform other actions
            } );
    }

    // Placeholder function for loading user activities
    function loadUserActivities ( userId )
    {
        // Perform an API request to load user activities
        fetch( `/api/user_activities/${ userId }` )
            .then( response =>
            {
                if ( !response.ok )
                {
                    throw new Error( 'Network response was not ok' );
                }
                return response.json();
            } )
            .then( data =>
            {
                console.log( 'User activities loaded successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error => console.error( 'Error loading user activities:', error ) );
    }

    // Placeholder function for adding a user
    function addUser ( username, email )
    {
        // Perform an API request to add a user
        fetch( '/api/add_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify( { username: username, email: email } ),
        } )
            .then( response => response.json() )
            .then( data =>
            {
                console.log( 'User added successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error =>
            {
                console.error( 'Error adding user:', error );
                // Handle errors, show an alert, or perform other actions
            } );
    }

    // Placeholder function for viewing user log
    function viewUserLog ( userId )
    {
        // Perform an API request to view user log
        fetch( `/api/view_user_log/${ userId }` )
            .then( response =>
            {
                if ( !response.ok )
                {
                    throw new Error( 'Network response was not ok' );
                }
                return response.json();
            } )
            .then( data =>
            {
                console.log( 'User log viewed successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error => console.error( 'Error viewing user log:', error ) );
    }

    // Placeholder function for approving a rating
    function approveRating ( ratingId )
    {
        // Perform an API request to approve a rating
        fetch( `/api/approve_rating/${ ratingId }`, {
            method: 'PUT',
        } )
            .then( response => response.json() )
            .then( data =>
            {
                console.log( 'Rating approved successfully:', data );
                // You can update the UI or perform other actions based on the response
            } )
            .catch( error =>
            {
                console.error( 'Error approving rating:', error );
                // Handle errors, show an alert, or perform other actions
            } );
    }

    // Initial data fetching and user table initialization
    fetchUserData()
        .then( userData =>
        {
            console.log( 'User Data:', userData );
            initializeUserTable( userData );
        } )
        .catch( error => console.error( 'Error fetching user data:', error ) );

    // Event delegation for user actions
    document.addEventListener( 'click', function ( event )
    {
        if ( event.target.matches( '.update-permissions-btn' ) )
        {
            // Extract user ID and new permissions from the UI
            const userId = event.target.getAttribute( 'data-user-id' );
            const newPermissions = prompt( 'Enter new permissions:' );
            updatePermissions( userId, newPermissions );
        } else if ( event.target.matches( '.delete-user-btn' ) )
        {
            // Extract user ID from the UI
            const userId = event.target.getAttribute( 'data-user-id' );
            deleteUser( userId );
        } else if ( event.target.matches( '.load-activities-btn' ) )
        {
            // Extract user ID from the UI
            const userId = event.target.getAttribute( 'data-user-id' );
            loadUserActivities( userId );
        } else if ( event.target.matches( '.add-user-btn' ) )
        {
            // Example of adding a new user
            const username = prompt( 'Enter username:' );
            const email = prompt( 'Enter email:' );
            addUser( username, email );
        } else if ( event.target.matches( '.view-user-log-btn' ) )
        {
            // Extract user ID from the UI
            const userId = event.target.getAttribute( 'data-user-id' );
            viewUserLog( userId );
        } else if ( event.target.matches( '.approve-rating-btn' ) )
        {
            // Extract rating ID from the UI
            const ratingId = event.target.getAttribute( 'data-rating-id' );
            approveRating( ratingId );
        }
    } );
} );





// /*C:\Users\Oleg\Desktop\ci-fsf-hotel-booking\hotels_booking\static\js\api\API.js*/


// $( document ).ready( async function ()
// {
//     console.log( 'API_hotels.js is running.' );
//     console.log( 'jQuery version:', $.fn.jquery );

//     const url = 'https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates?filter_by_currency=EUR&locale=en-us&room_number=1&checkin_date=2024-03-25&checkout_date=2024-03-26&longitude=-9.504427&adults_number=2&latitude=52.059935&order_by=popularity&units=metric&categories_filter_ids=class%3A%3A2%2Cclass%3A%3A4%2Cfree_cancellation%3A%3A1&include_adjacency=true&children_number=2&children_ages=5%2C0';

//     try
//     {
//         const response = await fetch( url, {
//             method: 'GET',
//             headers: {
//                 'X-RapidAPI-Key': '379883e8camsh2498a6dd4d55c4fp177937jsn7bfe4f4983db',
//                 'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
//             }
//         } );

//         if ( !response.ok )
//         {
//             throw new Error( `HTTP error! Status: ${ response.status }` );
//         }

//         const responseData = await response.json();
//         console.log( 'Response Data:', responseData );

//         // Check if "result" property exists and is an array
//         if ( responseData.result && Array.isArray( responseData.result ) )
//         {
//             const container = $( '#hotelContainer' );

//             // Display hotel cards with more detailed information
//             responseData.result.forEach( hotel =>
//             {
//                 const hotelCard = $( '<div class="hotel-container">' +
//                     '<div class="hotel-card">' +
//                     `<h2>${ hotel.hotel_name }</h2>` +
//                     `<p>${ hotel.address_trans }</p>` +
//                     `<p>Review Score: ${ hotel.review_score }</p>` +
//                     `<p>Price: ${ hotel.composite_price_breakdown.net_amount.amount_rounded } ${ hotel.composite_price_breakdown.net_amount.currency }</p>` +
//                     // Include more details
//                     '<h3>Additional Details:</h3>' +
//                     `<p>City: ${ hotel.city }</p>` +
//                     `<p>Country: ${ hotel.country_trans }</p>` +
//                     `<p>Distance to City Center: ${ hotel.distance_to_cc } km</p>` +
//                     `<p>Number of Reviews: ${ hotel.review_nr }</p>` +
//                     `<p>Room Type: ${ hotel.unit_configuration_label }</p>` +
//                     `<p>Is Free Cancellable: ${ hotel.is_free_cancellable ? 'Yes' : 'No' }</p>` +
//                     `<p>Is Genius Deal: ${ hotel.is_genius_deal ? 'Yes' : 'No' }</p>` +
//                     `<p>Class: ${ hotel.class }</p>` +
//                     `<p>Preferred: ${ hotel.preferred ? 'Yes' : 'No' }</p>` +
//                     `<p>Is Mobile Deal: ${ hotel.is_mobile_deal ? 'Yes' : 'No' }</p>` +
//                     // Display more deep details as needed
//                     '</div>' +
//                     '</div>' );

//                 // Display a maximum of 3 hotel photos
//                 hotelCard.append( '<h4>Photos:</h4><div class="hotel-photos">' );

//                 // Display hotel main photo
//                 if ( hotel.main_photo_url )
//                 {
//                     hotelCard.append( `<img src="${ hotel.main_photo_url }" alt="${ hotel.hotel_name } Photo">` );
//                 }

//                 // Display up to 2 additional photos
//                 if ( hotel.photos && hotel.photos.length > 0 )
//                 {
//                     for ( let i = 0; i < Math.min( 2, hotel.photos.length ); i++ )
//                     {
//                         hotelCard.append( `<img src="${ hotel.photos[ i ].url }" alt="${ hotel.hotel_name } Photo">` );
//                     }
//                 }

//                 hotelCard.append( '</div>' );

//                 container.append( hotelCard );
//             } );
//         } else
//         {
//             throw new Error( 'Invalid response data. Expected an array.' );
//         }
//     } catch ( error )
//     {
//         console.error( 'Error fetching hotel data:', error.message );
//     }
// } );
