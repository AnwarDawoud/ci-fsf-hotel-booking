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

let isEnlargedVisible = false;

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

    enlargedImage.src = imageSrc;
    enlargedContainer.style.display = 'flex';
    currentHotelId = hotelId;

    function hideEnlarged ()
    {
        enlargedContainer.style.display = 'none';
        isEnlargedVisible = false;
        document.getElementById( 'leftArrow' ).removeEventListener( 'click', showPreviousImage );
        document.getElementById( 'rightArrow' ).removeEventListener( 'click', showNextImage );
    }

    enlargedContainer.onclick = hideEnlarged;
    isEnlargedVisible = true;

    function showNextImage ()
    {
        const currentIndex = allImages.findIndex( img => img.src === enlargedImage.src );
        const nextIndex = ( currentIndex + 1 ) % allImages.length;

        if ( allImages[ nextIndex ] )
        {
            enlargedImage.src = allImages[ nextIndex ].src;
        }
    }

    function showPreviousImage ()
    {
        const currentIndex = allImages.findIndex( img => img.src === enlargedImage.src );
        const previousIndex = ( currentIndex - 1 + allImages.length ) % allImages.length;

        if ( allImages[ previousIndex ] )
        {
            enlargedImage.src = allImages[ previousIndex ].src;
        }
    }

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
