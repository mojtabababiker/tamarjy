$(document).ready(() => {
    // document manipulation section
    // Toggle nav bar
    $('#toggler').click(() => {
        $('#nav_bar').hasClass('hidden') ? $('#nav_bar').removeClass('hidden')
        .addClass('flex') : $('#nav_bar').addClass('hidden').removeClass('flex');
    });
    // Scroll to section
    $('body a').each((index ,e) =>{
        $(e).on('click',() => {
            $('#nav_bar').addClass('hidden').removeClass('flex');
            let divId = $(e).attr('href');
            div = document.getElementById(divId);
            console.log(divId);
            div.scrollIntoView({behavior: "smooth"});
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
                    diseases.forEach((disease) => {
                        diseasesNav.append(
                            '<li class="w-full min-w-fit decoration-0 p-2 m-0 list-none border-2 border-slate-200 rounded-lg cursor-pointer"' +
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
