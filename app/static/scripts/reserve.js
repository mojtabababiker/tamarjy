$(document).ready(() => {
    // document manipulation section
    // Toggle nav bar
    $('#toggler').click(() => {
        $('#nav_bar').hasClass('hidden') ? $('#nav_bar').removeClass('hidden')
        .addClass('flex') : $('#nav_bar').addClass('hidden').removeClass('flex');
    });
    // Scroll to section
    $('section a').each((index ,e) =>{
        $(e).on('click',() => {
            $('#nav_bar').addClass('hidden').removeClass('flex');
            let divId = $(e).attr('href');
            div = document.getElementById(divId);
            console.log(divId);
            div.scrollIntoView({behavior: "smooth"});
        });
    });
    // by default the first disease is selected and the clinics for that disease are displayed
    $('#diseases_nav li').first().addClass('bg-cyan-700').removeClass('bg-cyan-900');
    let specialty = [];  // the selected and displayed specialties
    const url = 'http://localhost:5050/api/v1';
    const userId = $('#user_id').data('userid');
    specialty.push($('#diseases_nav').children().first().data('specialty'));
    // set a click event for each disease that will display the clinics for it
    // using the clinics API endpoint TODO: add the this endpoint to the backend
    $('#diseases_nav').children().each((index, element) => {
        console.log(element);
        $(element).on('click', () => {
            let skip = false;  // flag to skip the specialty if it is already selected TODO: add this feature
            // set the selected disease as active and the others as inactive
            $('#diseases_nav li').each((index, i) => {
                $(i).addClass('bg-cyan-900').removeClass('bg-cyan-700');
            });
            $(element).addClass('bg-cyan-700').removeClass('bg-cyan-900');
            // push the selected specialty to the specialty array if it's not already there
            if (specialty.includes($(element).data('specialty'))) {
                skip = true;
            } else {
                specialty.push($(element).data('specialty'));
                skip = false;
            }
            console.log(specialty);
            if (true) {
                // get the clinics for the selected specialty
                $.get(url + `/clinics?specialty=${$(element).data('specialty')}&user_id=${userId}`, (data) => {
                    console.log(data.data);
                    if (data.status) {
                        // TODO: cache the clinics data to avoid multiple requests
                        // clear the clinics div
                        $('#clinics').html('');
                        $('#clinics').html(`<!-- reservation message --> 
                        <div class="w-full shrink-0 m-0 p-0 mx-auto text-center hidden" id="reservation_message">
                            <h3 class="w-full md:w-1/2 mx-auto text-lg md:text-2xl text-center text-opacity-75 text-slate-950"></h3>
                        </div>`);
                        console.log("status: ", data.status);
                        // append the clinics to the clinics div
                        data.data.forEach((clinic) => {
                            // TODO: add the clinic available appointments element (date and time)
                            $('#clinics').append(
                                `<div class="w-full h-72 md:h-80 md:w-[32%] md:mx-[0.65%] rounded-lg shadow-slate-500 bg-blend-multiply cursor-pointer
                                            flex flex-col justify-center items-center overflow-hidden object-fill bg-center bg-cover bg-no-repeat
                                            hover:shadow-slate-800 hover:bg-blend-multiply hover:bg-opacity-75 hover:bg-slate-800 clinic-card"
                                      style="background-image: url(/static/images/clinics_images/${clinic.image})">
                                    <!-- clinic details -->
                                    <div class="w-full h-full flex flex-col justify-center px-2 pt-3 m-0 bg-slate-800 bg-opacity-30 text-slate-100 z-0">
                                        <h3 class="text-2xl text-center text-opacity-75 font-bold tracking-wider drop-shadow-2xl z-0">${ clinic.name }</h3>
                                    </div>
                                    <div class="w-full flex flex-col justify-center p-2 bg-slate-200 border-1 border-slate-800 border-opacity-50 border-t-0 rounded-lg">
                                        <p class="text-sm text-left text-opacity-65 font-bold inline-block">Specialty: <span class="text-opacity-100 font-normal">${clinic.specialty}</span></p>
                                        <p class="text-sm text-left text-opacity-65 font-bold inline-block">Phone: <span class="text-opacity-100 font-normal">${clinic.phone}</span></p>
                                    </div>
                                    <!-- TODO: clinic available dates -->
                                    <!-- reserve -->
                                    <button class="hidden reserve" data-clinicid="${clinic.id}">Reserve</button>
                                </div>`
                            )}
                        );
                    } else {
                        // TODO: add a message to the user if there are no clinics for the selected specialty
                    }
                })
                .then(() => {
                    // click event on the clinics cards
                    $('.clinic-card').each((index, element) => {
                        $(element).on('click', () => {
                            const clinicId = $(element).children().last().data('clinicid');
                            console.log(clinicId);
                            // reserve an appointment for the user
                            // TODO: add the date selected by the user to the request
                            $.ajax({
                                url: url + '/clinics/reserve',
                                type: 'POST',
                                data: JSON.stringify({clinic_id: clinicId, user_id: userId}),
                                dataType: 'json',
                                contentType: 'application/json',
                                success: (data) => {
                                    $('#reservation_message h3').addClass('text-green-500').text(data.message);
                                    $('#reservation_message').removeClass('hidden').addClass('block');
                                },
                                error: (data) => {
                                    $('#reservation_message h3').addClass('text-red-500') .text(data.error);
                                    $('#reservation_message').removeClass('hidden').addClass('block');
                                }
                            });
                        });
                    });
                })
            } else {
                // TODO: load the clinics from the cache
                alert('Specialty already selected');
            };
        });
    });
    // click event on the clinics cards
    $('.clinic-card').each((index, element) => {
        $(element).on('click', () => {
            const clinicId = $(element).children().last().data('clinicid');
            // reserve an appointment for the user
            // TODO: add the date selected by the user to the request
            $.ajax({
                url: url + '/clinics/reserve',
                type: 'POST',
                data: JSON.stringify({clinic_id: clinicId, user_id: userId}),
                dataType: 'json',
                contentType: 'application/json',
                success: (data) => {
                    $('#reservation_message h3').addClass('text-green-500').text(data.message);
                    $('#reservation_message').removeClass('hidden').addClass('block');
                },
                error: (data) => {
                    $('#reservation_message h3').addClass('text-red-500') .text(data.error);
                    $('#reservation_message').removeClass('hidden').addClass('block');
                }
            });
        });
    });
});