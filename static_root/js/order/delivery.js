

const chosenPrice = document.querySelector('.delivery_chosen_price')
const totalProductsPrice =     document.querySelector('.total_products_price')
const totalPiceWithDelivery =  document.querySelector('.total_price_with_delivery')
var adressList = []
var delivery = undefined

const cdekPrice =    document.getElementById('cdek_price')
const ruspostPrice = document.getElementById('ruspost_price')

const deliveryMethods =      document.querySelectorAll('.delivery_methods__item')
const deliveryMethodInputs = document.querySelectorAll('input[name="order_delivery_method"]') 



function adressListOnLoad(data) {
    let adressPreview = undefined
    console.log(data);
    
    if (data['adress_list'].length > 0) {
        adressList = data['adress_list']
        adressPreview = nunjucks.renderString(deliveryAdressPreview, {adress :  adressList[0]});
    }
    if (data['delivery']) {
        delivery = data['delivery']
        ruspostPrice.innerHTML = delivery['ruspost']
        cdekPrice.innerHTML =    delivery['cdek']
    } 

    function set_method_adress(method, html) {
        if (adressPreview != undefined) { 
            method.dataset.adress = true
            method.querySelector('.adress_prev').innerHTML = adressPreview
        } else { 
            method.dataset.adress = false
        }
    }
        
    for (let method of deliveryMethods) {
        set_method_adress(method, adressPreview)
    }
    
}

function AdressBlankForm() {
    popupOpen()
    PopupInner.innerHTML = nunjucks.renderString(deliveryAdressForm, {change : false, url : deliveryAdressURlUpdate});
    let form = PopupInner.querySelector('form')
    formValidate(form)
}

function AdressChange(i) {
    popupOpen()
    PopupInner.innerHTML = nunjucks.renderString(deliveryAdressForm, {change : true, url : deliveryAdressURlUpdate, adress : adressList[i]});
    let form = PopupInner.querySelector('form')
    formValidate(form)
    let backToList = PopupInner.querySelector('.back_to_list')
    if (backToList) {
        backToList.onclick = () => {
            AdressDataList()
        }
    }
}

function AdressUpdate(data) {
    popupClose()
    adressList = data
    adressListOnLoad(adressList)
}

function AdressSet(data) {
    adressList = data['adress_list']
    let template = nunjucks.renderString(deliveryAdressPreview, {adress :  adressList[0]});
    for (let prev of adressPrev) {
        prev.innerHTML = template
    }
    AdressDataList()
    popupClose()
}


// List of saved adress
function AdressDataList() {
    if (userAuthenticated) {
        PopupInner.innerHTML = nunjucks.renderString(deliveryAdressList, {adress_list : adressList, url : deliveryAdressURlSet});
        PopupWrapper.classList.add('active')
        form = PopupInner.querySelector('form')
        formValidate(form)
       
        let changeButton = PopupInner.querySelectorAll('.change')
        for (let i = 0; i < changeButton.length; i++) {
            let change = changeButton[i];
            change.onclick = () => {
                AdressChange(i)
            }
        }
        let addAdress = PopupInner.querySelector('.add_adress')
        addAdress.onclick = () => {
            AdressBlankForm() 
        }
    } else {
        if (adressList.length > 0) {
            AdressChange(0)
        } else {
             AdressBlankForm() 
        }
        
    }
    
}
async function initPostData() {
    let response = await fetch(deliveryAdressUrlGet, {})
        response = await response.json();
        adressListOnLoad(response['data'])
} 
initPostData()


// DeliveryMethods
function deliveryMethodSelected(i) {
    for (let j = 0; j < deliveryMethods.length; j++) {
        let method = deliveryMethods[j];
        if (i == j) { method.dataset.selected = true } else { method.dataset.selected = false }
    }
}

function set_delivery_price(input)  {
    if (delivery != undefined) {
        console.log(input.dataset.key);
        chosenPrice.innerHTML = delivery[input.dataset.key];
        console.log(parseInt(totalProductsPrice.innerHTML),parseInt(chosenPrice.innerHTML));
        totalPiceWithDelivery.innerHTML = parseInt(totalProductsPrice.innerHTML.replace(' ','')) + parseInt(chosenPrice.innerHTML.replace(' ',''))
    }
}


function checkDeliveryChecked() {
    deliveryChecked = false
    for (let meth of deliveryMethodInputs) {
        if (meth.checked) {
            deliveryChecked = true
            break
        }
    }
    if (deliveryChecked == true) {
        orderBtnWrp.classList.remove('disabled')
    } else {
        orderBtnWrp.classList.add('disabled')
    }
}

for (let i = 0; i < deliveryMethodInputs.length; i++) {
    let input = deliveryMethodInputs[i];
    input.onchange = () => {
        checkDeliveryChecked()
        set_delivery_price(input)
        if (adressList.length == 0) {
            AdressBlankForm()
            input.checked = false
        } 
        deliveryMethodSelected(i)
    }
    if (input.checked) {
        
        deliveryMethodSelected(i)
        set_delivery_price(input)
    }
}
checkDeliveryChecked()