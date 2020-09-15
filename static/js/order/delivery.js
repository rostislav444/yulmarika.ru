

const chosenPrice = document.querySelector('.delivery_chosen_price')
var   chosenPriceParent = undefined
if (chosenPrice) {
    chosenPriceParent = chosenPrice.parentElement
}
const totalProductsPrice =     document.querySelector('.total_products_price')
const totalPiceWithDelivery =  document.querySelector('.total_price_with_delivery')
var adressList = []
var delivery = undefined
const cdekPrice =    document.getElementById('cdek_price')
const ruspostPrice = document.getElementById('ruspost_price')

const deliveryMethods =      document.querySelectorAll('.delivery_methods__item')
const deliveryMethodInputs = document.querySelectorAll('input[name="order_delivery_method"]') 
const minimalFreeDeliveryTotal = parseInt(document.querySelector('.free_delivery_price').dataset.price)

var methSelected = undefined


function adressListOnLoad(data) {
    let adressPreview = undefined
    
    if (data['adress_list'].length > 0) {
        adressList = data['adress_list']
        adressPreview = nunjucks.renderString(deliveryAdressPreview, {adress :  adressList[0]});
    }
    if (data['delivery']) {
        delivery = data['delivery']
       
        for (let meth of deliveryMethods) {
            if (adressList.length > 0 && deliveryMethods.length > 1) {
                if (parseInt(delivery[meth.dataset.key]) == 0) {
                    meth.style.display = 'none'
                    meth.classList.add('active')
                } else {
                    meth.style.display = 'grid'
                    meth.classList.add('active')
                }
            }
            if (adressList.length == 0) {
                if (parseInt(delivery[meth.dataset.key]) == 0) {
                    meth.classList.remove('active')
                } else {
                    meth.classList.add('active')
                }
            }
            methPrice = meth.querySelector('.method_price')
            if (methPrice) {
                methPrice.innerHTML = delivery[meth.dataset.key]
            }
            // If user previously selected some method
           
            if (methSelected !== undefined) {
                console.log(deliveryMethodInputs[methSelected]);
                deliveryMethodInputs[methSelected].checked = true
                checkDeliveryChecked()
            }
           
        }
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
    PopupInner.innerHTML = nunjucks.renderString(deliveryAdressForm, {change : false, url : deliveryAdressURlUpdate, adress : userBaseData});
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
    if (data['delivery']) {
        delivery = data['delivery']
        if (ruspostPrice) {
            ruspostPrice.innerHTML = delivery['ruspost']
        }
        if (cdekPrice) {
            cdekPrice.innerHTML = delivery['cdek']
        }
        for (let input of document.querySelectorAll('input[name="order_delivery_method"]')) {
            if (input.checked) {
                set_delivery_price(input)
                break
            }
        }
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
                change.onclick = () => { AdressChange(i) }
        }
        let addAdress = PopupInner.querySelector('.add_adress')
            addAdress.onclick = () => { AdressBlankForm() }
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
        if (freeDelivery == false) {
            if (chosenPrice) {
                chosenPrice.innerHTML = delivery[input.dataset.key];
            }
            
            totalPiceWithDelivery.innerHTML = parseInt(totalProductsPrice.dataset.price) + parseInt(chosenPrice.innerHTML.replace(' ',''))
        } else {
            if (chosenPriceParent) {
                chosenPriceParent.innerHTML = 'Бесплатно'
            }
            totalPiceWithDelivery.innerHTML = parseInt(totalProductsPrice.dataset.price)
        }
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
        methSelected = i
        set_delivery_price(input)
        if (adressList.length == 0) {
            input.checked = false
            
            AdressBlankForm()
        } else {
            checkDeliveryChecked()
        }
        deliveryMethodSelected(i)
        makeBigNum()
    }
    if (input.checked) {
        
        deliveryMethodSelected(i)
        set_delivery_price(input)
    }
}
checkDeliveryChecked()