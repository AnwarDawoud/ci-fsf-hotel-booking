$( document ).ready( async function ()
{
    console.log( 'API_hotels.js is running.' );
    console.log( 'jQuery version:', $.fn.jquery );

    const url = 'https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates?filter_by_currency=EUR&locale=en-us&room_number=1&checkin_date=2024-03-25&checkout_date=2024-03-26&longitude=-9.504427&adults_number=2&latitude=52.059935&order_by=popularity&units=metric&categories_filter_ids=class%3A%3A2%2Cclass%3A%3A4%2Cfree_cancellation%3A%3A1&include_adjacency=true&children_number=2&children_ages=5%2C0';

    try
    {
        const response = await fetch( url, {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': '379883e8camsh2498a6dd4d55c4fp177937jsn7bfe4f4983db',
                'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
            }
        } );

        if ( !response.ok )
        {
            throw new Error( `HTTP error! Status: ${ response.status }` );
        }

        const responseData = await response.json();
        console.log( 'Response Data:', responseData );

        // Check if "result" property exists and is an array
        if ( responseData.result && Array.isArray( responseData.result ) )
        {
            const container = $( '#hotelContainer' );

            // Display hotel cards with more detailed information
            responseData.result.forEach( hotel =>
            {
                const hotelCard = $( '<div class="hotel-container">' +
                    '<div class="hotel-card">' +
                    `<h2>${ hotel.hotel_name }</h2>` +
                    `<p>${ hotel.address_trans }</p>` +
                    `<p>Review Score: ${ hotel.review_score }</p>` +
                    `<p>Price: ${ hotel.composite_price_breakdown.net_amount.amount_rounded } ${ hotel.composite_price_breakdown.net_amount.currency }</p>` +
                    // Include more details
                    '<h3>Additional Details:</h3>' +
                    `<p>City: ${ hotel.city }</p>` +
                    `<p>Country: ${ hotel.country_trans }</p>` +
                    `<p>Distance to City Center: ${ hotel.distance_to_cc } km</p>` +
                    `<p>Number of Reviews: ${ hotel.review_nr }</p>` +
                    `<p>Room Type: ${ hotel.unit_configuration_label }</p>` +
                    `<p>Is Free Cancellable: ${ hotel.is_free_cancellable ? 'Yes' : 'No' }</p>` +
                    `<p>Is Genius Deal: ${ hotel.is_genius_deal ? 'Yes' : 'No' }</p>` +
                    `<p>Class: ${ hotel.class }</p>` +
                    `<p>Preferred: ${ hotel.preferred ? 'Yes' : 'No' }</p>` +
                    `<p>Is Mobile Deal: ${ hotel.is_mobile_deal ? 'Yes' : 'No' }</p>` +
                    // Display more deep details as needed
                    '</div>' +
                    '</div>' );

                // Display a maximum of 3 hotel photos
                hotelCard.append( '<h4>Photos:</h4><div class="hotel-photos">' );

                // Display hotel main photo
                if ( hotel.main_photo_url )
                {
                    hotelCard.append( `<img src="${ hotel.main_photo_url }" alt="${ hotel.hotel_name } Photo">` );
                }

                // Display up to 2 additional photos
                if ( hotel.photos && hotel.photos.length > 0 )
                {
                    for ( let i = 0; i < Math.min( 2, hotel.photos.length ); i++ )
                    {
                        hotelCard.append( `<img src="${ hotel.photos[ i ].url }" alt="${ hotel.hotel_name } Photo">` );
                    }
                }

                hotelCard.append( '</div>' );

                container.append( hotelCard );
            } );
        } else
        {
            throw new Error( 'Invalid response data. Expected an array.' );
        }
    } catch ( error )
    {
        console.error( 'Error fetching hotel data:', error.message );
    }
} );
