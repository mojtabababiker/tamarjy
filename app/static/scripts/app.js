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
            const divId = $(e).attr('href');
            const div = document.getElementById(divId);
            div.scrollIntoView({behavior: "smooth"});
        });
    });
    // create reserve GET method and set the diseases cookie
    $('#save_cookie').on('click', () => {
	// get the diseases and send them to the server as http header
        let diseases = [];
        $('#diseases_nav li').each((index, e) => {
            diseases.push(e.id);
        });
	console.log(diseases);
	console.log(window.location.host);
        // set the Diseases-Ids header and send the request
        $.ajax({
            url: `http://${window.location.host}/set_cookie`,
            type: 'GET',
            headers: {'Diseases-Ids': diseases.join(', ')},
            success: (data) => {
                alert(data.status)
                $('#reserve')[0].click()
            }
        });
    });
    // API section
    const url = 'http://localhost:5050/api/v1';
    const resultDiv = $('#results'); // Result (div) container
    const diseasesNav = $('#diseases_nav'); // Diseases (ul) nav bar
    const diseaseDesc = $('#disease_desc p'); // Disease description (p) paragraph
    const diseasePrec = $('#disease_prec p'); // Disease precautions (p) paragraph

    function getDiseasesInfo(e){
	    console.log($(this))
        $('#diseases_nav li').each((index, e) => {
            $(e).addClass('bg-cyan-900').removeClass('bg-cyan-700');
        });
        $(this).addClass('bg-cyan-700').removeClass('bg-cyan-900');
        $.ajax({
            url: url + '/diseases/' + $(this).attr('id'),
            type: 'GET',
	    contentType: 'application/json',
	    dataType: "json",
            success: (data) => {
                diseaseDesc.text(data.description);
                diseasePrec.text(data.precautions);
            },
            error: (error) => {
                alert(`An error occurred: ${error.text}`)
                resultDiv.addClass('hidden').removeClass('flex');
            }
        }).then(() => {
	    resultDiv.removeClass('hidden').addClass('flex');
	    document.getElementById("results").scrollIntoView({behavior: "smooth"});
	});
    }
    $('#predict').click(() => {
        let symptoms = $('#symptoms').val();
        if(symptoms){
            $.ajax({
                url: url + '/predict',
                type: 'POST',
		        contentType: 'application/json',
                data: JSON.stringify({symptoms: symptoms}),
		        dataType: "json",
                success: (data) => {
                    // list of objects [{disease_name: 'name', disease_id: '1234-abcd', probability: 0.0}]
                    const diseases = data.diseases;
		            console.log(diseases)
                    if (diseases.length > 0){
                        diseasesNav.empty();
                    }
                    diseases.forEach((disease) => {
                        diseasesNav.append(
                            '<li class="w-full min-w-fit decoration-0 p-2 m-0 list-none border-2 border-slate-200 rounded-lg cursor-pointer bg-cyan-900 hover:bg-cyan-700 transition-all duration-300"' +
                            `id=${disease.disease_id}>` + disease.disease_name + '</li>'
                            )
                        // Add click event to each disease item
                        $(`#${disease.disease_id}`).on('click', getDiseasesInfo);
                    })
                },
                error: (error, data) => {
                    alert(`An error occurred---: ${data.text}`)
                    resultDiv.addClass('hidden').removeClass('flex');
                    },
            }).then(() => {
                let firstDisease = diseasesNav.children().first();
                if (firstDisease){
                    firstDisease.click();
                    resultDiv.removeClass('hidden').addClass('flex');
                }
            })
        } 
        else {
            alert('Please fill all fields');
        };
    });
});
