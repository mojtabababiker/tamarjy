$(document).ready(() => {
    // disable the submit button
    $(':submit').prop('disabled', true);
    // display a prompt to the user to enable the location
    $('#pop-up').removeClass('hidden').addClass('flex');

    // get the user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            // on success enable the submit button and save the user location
            $(':submit').prop('disabled', false);
            $('#pop-up').removeClass('flex').addClass('hidden');
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
    }
});