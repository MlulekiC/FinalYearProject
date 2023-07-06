console.log('Hello world!')

// districts-json
const districtDataBox = document.getElementById('district-data-box')
const districtInput = document.getElementById('districts')

// municipality-json
const municipalityDataBox = document.getElementById('municipality-data-box')
const municipalityInput = document.getElementById('municipalities')

const municipalityText = document.getElementById('municipality-text')

// town-json
const townDataBox = document.getElementById('town-data-box')
const townInput = document.getElementById('towns')
const townText = document.getElementById('town-text')


$.ajax({
    type: 'GET',
    url: '/users/districts-json/',
    success: function(response){
        console.log(response.data)
        const DistrictData = response.data
        DistrictData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            districtDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})

districtInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedDistrict = e.target.value

    municipalityDataBox.innerHTML = ""
    municipalityText.textContent = "Choose local Municipality"
    municipalityText.classList.add("default")


    $.ajax({
        type: 'GET',
        url: `municipalities-json/${selectedDistrict}/`,
        success: function(response){
            console.log(response.data)
            const municipalityData = response.data
            municipalityData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                municipalityDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })

})

municipalityInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedMunicipality = e.target.value

    townDataBox.innerHTML = ""
    townText.textContent = "Choose local Municipality"
    townText.classList.add("default")

    $.ajax({
        type: 'GET', 
        url: `towns-json/${selectedMunicipality}/`,
        success: function(response){
            console.log(response.data)
            const townData = response.data
            townData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                townDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})
