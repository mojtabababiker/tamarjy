$(document).ready(() => {
    // disable the submit button
    $(':submit').prop('disabled', true);
    // display a prompt to the user to enable the location
    // $('#pop-up').removeClass('hidden').addClass('flex');
    Swal.fire({
        title: 'Press allow location access',
        text: `Tamarjy uses your location to allocate the nearest health care providers. 
                Please allow location access to continue.`,
        icon: 'info',
        allowEscapeKey: false,
        allowOutsideClick: false,
        showConfirmButton: false,
        showCancelButton: false,
        showCloseButton: false,
        id: 'pop-up',
    })

    // get the user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            // on success enable the submit button and save the user location
            $(':submit').prop('disabled', false);
            // $('#pop-up').removeClass('flex').addClass('hidden');
            Swal.close();
            // add user location coordinates to the form
            $('#latitude').val(position.coords.latitude);
            $('#longitude').val(position.coords.longitude);
            console.log('Latitude: ' + position.coords.latitude);
            console.log('Longitude: ' + position.coords.longitude);
        });
    } else {
        console.log('Geolocation is not supported by this browser.');
        $('#pop-up').removeClass('border-cyan-950').addClass('border-red-700');
        $('#pop-up p').text('Geolocation is not supported by this browser. Please choose another browser.');
        $('#pop-up').removeClass('hidden').addClass('flex');
    }
    $('#pick_img_btn').on('click', () => {
        $('#pick_img').click();
    });
});