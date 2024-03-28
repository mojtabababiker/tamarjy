$(document).ready(() => {
    // by default the first disease is selected and the clinics for that disease are displayed
    $('#diseases_nav').children().first().addClass('bg-cyan-950').removeClass('bg-cyan-800');
    const specialty = [];  // the selected and displayed specialties
    const url = 'http://localhost:5050/api/v1';
    const userId = $('#user_id').data('userId');
    specialty.push($('#diseases_nav').children().first().data('specialty'));
    // set a click event for each disease that will display the clinics for it
    // using the clinics API endpoint TODO: add the this endpoint to the backend
    $('#diseases_nav').children().each((index, element) => {
        $(element).on('click', () => {
            let skip = false;  // flag to skip the specialty if it is already selected TODO: add this feature
            // set the selected disease as active and the others as inactive
            $('#diseases_nav').children().each((index, element) => {
                $(element).addClass('bg-cyan-800').removeClass('bg-cyan-950');
            });
            $(this).addClass('bg-cyan-950').removeClass('bg-cyan-800');
            // push the selected specialty to the specialty array if it's not already there
            specialty.includes($(this).data('specialty')) ? skip = true : specialty.push($(this).data('specialty'));
            if (!skip) {
                // get the clinics for the selected specialty
                $.get(url + `/clinics?specialty=${$(this).data('specialty')}&user_id=${userId}`, (data) => {
                    if (data.status === 'success') {
                        // TODO: cache the clinics data to avoid multiple requests
                        // clear the clinics div
                        $('#clinics').html('');
                        // append the clinics to the clinics div
                        data.forEach((clinic) => {
                            // TODO: add the clinic available appointments element (date and time)
                            $('#clinics').append(
                                `<div class="w-full h-72 md:h-80 md:w-[30%] m-2 md:m-0 rounded-lg border-2 border-opacity-65 border-cyan-700
                                flex flex-col overflow-hidden">
                                <!-- clinic info -->
                                <div class="w-full h-1/2 flex flex-row m-0 p-0">
                                    <!-- clinic image -->
                                    <img src="/static/images/clinics_images/${clinic.image}" alt="clinic image" class="w-full object-cover m-0 p-0">
                                </div>
                                <!-- clinic details -->
                                <div class="w-full flex flex-col justify-start pl-2 m-0 mt-2">
                                    <h3 class="text-xl text-center text-opacity-75 font-bold">${clinic.name}</h3>
                                    <p class="text-sm text-left text-opacity-65 font-bold inline-block">Specialty: <span class="text-opacity-100 font-normal">${clinic.specialty}</span></p>
                                    <p class="text-sm text-left text-opacity-65 font-bold inline-block">Phone: <span class="text-opacity-100 font-normal">${clinic.phone}</span></p>
                                </div>
                                <!-- reserve -->
                                <div class="w-full align-bottom flex flex-row justify-center m-0 p-0">
                                    <button class="w-1/2 p-3 bg-cyan-700 text-slate-200 rounded-lg hover:bg-cyan-800 reserve" data-clinicId="${clinic.id}">Reserve</button>
                                </div>
                            </div>`
                            )}
                        );
                    } else {
                        // TODO: add a message to the user if there are no clinics for the selected specialty
                        alert(data.error);
                    }
                }
            )} else {
                // TODO: load the clinics from the cache
                alert('Specialty already selected');
            };
        });
    });
    // reserve button click event
    $('.reserve').each((index, element) => {
        element.on('click', () => {
            const clinicId = $(this).data('clinicId');
            // reserve an appointment for the user
            // TODO: add the date selected by the user to the request
            $.post(url + '/clinics/reserve', JSON.stringify({clinic_id: clinicId, user_id: userId}), (data) => {
                if (data.status === 'success') {
                    alert(data.message);
                    $('#reservation_message h3').addClass('text-green-500').text(data.message);
                    $('#reservation_message').removeClass('hidden').addClass('block');
                } else {
                    alert(data.error);
                    $('#reservation_message h3').addClass('text-red-500') .text(data.error);
                    $('#reservation_message').removeClass('hidden').addClass('block');
                }
            });
        });
    });
});