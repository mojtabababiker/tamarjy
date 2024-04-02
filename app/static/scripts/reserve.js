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
    
    // variables section
    // by default the first disease is selected and the clinics for that disease are displayed
    $('#diseases_nav li').first().addClass('bg-cyan-700').removeClass('bg-cyan-900');
    let specialty = [];  // the selected and displayed specialties
    const url = `http://${window.location.host}/api/v1`;
    const userId = $('#user_id').data('userid');
    specialty.push($('#diseases_nav').children().first().data('specialty'));

    // functions section
    // get the clinics for the selected specialty
    function getClinics(element) {
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
                                        hover:shadow-slate-800 hover:bg-blend-multiply hover:bg-opacity-75 hover:bg-slate-800 clinic-card transition-all duration-300"
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
                    $('#clinics').html('');
                    Swal.fire({
                        title: 'No clinics available on your region',
                        text: 'Please try again later',
                        icon: 'info',
                        confirmButtonText: 'Back home',
                        confirmButtonColor: '#3498db',
                        showCancelButton: true,
                        cancelButtonText: 'Choose another',
                    }).then(() => {
                        if (result.dismiss === Swal.DismissReason.cancel) {
                            return;
                        }
                        window.location.href = '/home';
                    });
                }
            })
            .then(() => {
                // click event on the clinics cards
                $('.clinic-card').each((index, element) => {
                    $(element).on('click', () => {
                        setReservation(element);
                    });
                });
            })
        } else {
            // TODO: load the clinics from the cache
            alert('Specialty already selected');
        };
    }
    // get the date selected by the user
    function getSelectedDate(clinicId) {
        return new Promise((resolve, reject) => {
            let time = '';
            let date = '';
            $.get(url + `/clinics/dates/${clinicId}`, (data) => {
                if (data.status === "success") {
                    $('#days').html('');
                    data.dates.forEach((date) => {
                        $('#days').append(`
                        <option value="${date}">${date}</option>
                        `)
                    });
                } else {
                    // alter the user with error message
                    reject('Error fetching dates');
                }
            }).then(() => {
                $('#days').on('change', () => {
                    date = $('#days').val();
                    $.get(url + `/clinics/dates/${clinicId}?day=${date}`, (data) => {
                        if (data.status === "success") {
                            // TODO: cache it before deleting
                            $('#times').html('');
                            data.times.forEach((time) => {
                                $('#times').append(
                                    `<div class="w-1/4 h-1/4 border border-slate-500 rounded flex justify-center items-center text-slate-200 bg-cyan-700
                                    hover:bg-cyan-900 hover:border-cyan-900 cursor-pointer transition-all duration-300">${time}</div>`
                                );
                            });
                            $('#times').children().each((index, element) => {
                                $(element).on('click', () => {
                                    $('#times').children().each((index, element) => {
                                        $(element).removeClass('bg-cyan-900').addClass('bg-cyan-700');
                                    });
                                    $(element).removeClass('bg-cyan-700').addClass('bg-cyan-900');
                                    time = $(element).text();
                                    console.log(time);
                                });
                            });
                        } else {
                            $('#times').html('');
                            $('#times').append(
                                `<div class="w-full h-1/2 p-3 border border-slate-500 rounded flex justify-center items-center text-slate-200 bg-cyan-700">No available times</div>`
                            );
                        }
                    });
                });
            }).then(() => {
                $('#days').trigger('change');
                $('#clinic_dates').removeClass('hidden').addClass('flex');
            });
            $('#reserve').on('click', () => {
                // get the datetime selected by the user
                if (!time) {
                    reject('Please select a time');
                }
                console.log(`${date}T${time}`);
                $('#clinic_dates').removeClass('flex').addClass('hidden');
                resolve(`${date}t${time}`);
            });
            $(document).on('keydown', (e) => {
                if (e.key === 'Escape') {
                    $('#clinic_dates').removeClass('flex').addClass('hidden');
                    reject('User cancelled the reservation');
                }
            });
        });
    }
    // set the reservation for the selected clinic
    function setReservation(element) {
        const clinicId = $(element).children().last().data('clinicid');
        console.log(clinicId);
        // get the date selected by the user
        getSelectedDate(clinicId)
            .then((date) => {
                // reserve an appointment for the user
                // TODO: add the date selected by the user to the request
                if (!date) {
                    // alert('Please select a date');
                    Swal.fire({
                        title: 'Please select a date',
                        text: 'The appointment date is required to reserve a clinic ',
                        icon: 'info',
                        confirmButtonText: 'Choose',
                        confirmButtonColor: '#3498db',
                        showCancelButton: true,
                        cancelButtonText: 'Back home',
                    }).then(() => {
                        if (result.dismiss === Swal.DismissReason.cancel) {
                            return;
                        }
                        window.location.href = '/home';
                    });
                    $('#reservation_message h3').addClass('text-red-500').text('Please select a date');
                    $('#reservation_message').removeClass('hidden').addClass('block');
                }
                $.ajax({
                    url: url + '/clinics/reserve',
                    type: 'POST',
                    data: JSON.stringify({ clinic_id: clinicId, user_id: userId, date: date }),
                    dataType: 'json',
                    contentType: 'application/json',
                    success: (data) => {
                        Swal.fire({
                            title: 'Reservation set successfully',
                            text: `Your appointment has been set successfully due ${date} at ${data.time}`,
                            icon: 'info',
                            confirmButtonText: 'Choose another',
                            confirmButtonColor: '#3498db',
                            showCancelButton: true,
                            cancelButtonText: 'Back home',
                        }).then(() => {
                            if (result.dismiss === Swal.DismissReason.cancel) {
                                return;
                            }
                            window.location.href = '/home';
                        });
                        $('#reservation_message h3').addClass('text-green-500').text(data.message);
                        $('#reservation_message').removeClass('hidden').addClass('block');
                    },
                    error: (data) => {
                        Swal.fire({
                            title: 'Error setting the reservation',
                            text: `${data.error}`,
                            icon: 'info',
                            confirmButtonText: 'Try again',
                            confirmButtonColor: '#3498db',
                            showCancelButton: true,
                            cancelButtonText: 'Back home',
                        }).then(() => {
                            if (result.dismiss === Swal.DismissReason.cancel) {
                                return;
                            }
                            window.location.href = '/home';
                        });
                        $('#reservation_message h3').addClass('text-red-500').text(data.error);
                        $('#reservation_message').removeClass('hidden').addClass('block');
                    }
                });
            })
            .catch((error) => {
                console.error(error);
            });
    }
    // set a click event for each disease that will display the clinics for it
    // using the clinics API endpoint TODO: add the this endpoint to the backend
    $('#diseases_nav').children().each((index, element) => {
        console.log(element);
        $(element).on('click', () => {
            getClinics(element);
        });
    });
    // click event on the clinics cards
    $('.clinic-card').each((index, element) => {
        $(element).on('click', () => {
            setReservation(element);
        });
    });
});