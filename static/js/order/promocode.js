


function promoCodeField(data, field) {
    data = JSON.parse(data)
    if (data['msg'] != undefined) {
        prormoCodeMessages.innerHTML = data['msg']
        if (data['success'] != undefined) {
            prormoCodeMessages.classList.add('active')
            if (data['success'] == true) {
                prormoCodeMessages.classList.add('success')
            }
        }
    } else {
        prormoCodeMessages.innerHTML = ''
        prormoCodeMessages.classList.remove('active')
        prormoCodeMessages.classList.remove('success')

    }
    if (data['cart']) {
        CartUpdate(data['cart'], true)
    }
    
}

const promoCodeForm = document.querySelector('#promocode_form')
const promoCodeInput = promoCodeForm.querySelector('#promocode__input')
const prormoCodeMessages = document.querySelector('.prormocode_messages')
promoCodeForm.onsubmit = (e) => {
    e.preventDefault()
    
    xhrOnLoad(
        method = 'POST',
        url = promoCodeForm.action,
        data = JSON.stringify({ 'text' : promoCodeInput.value }),
        func = promoCodeField,
        field = promoCodeInput
    )
   
}

pomoCodeBtn = document.querySelector('.pomo_code_button')
pomoCodeData = document.querySelector('.pomo_code_data')
pomoCodeBtn.onclick = () => {
    if (pomoCodeData.classList.contains('is_visible') == false) {
        pomoCodeData.classList.add('is_visible')
    } else {
        pomoCodeData.classList.remove('is_visible')
    }
}