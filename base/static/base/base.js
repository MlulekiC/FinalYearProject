console.log('Hello world!')


/////////////////////////////////////////////

const adminTownDataBox = document.getElementById('admin-town-data-box')
const adminTownInput = document.getElementById('admin-towns')


$.ajax({
    type: 'GET',
    url: '/towns-json/',
    success: function(response){
        console.log(response.data)
        const townData = response.data
        townData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            adminTownDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})


////////////////////////////////////////////////