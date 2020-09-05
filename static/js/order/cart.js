// Templates
const totalSaveTpl = "<p class='you_save'>Вы экономите {{ total_save }} RUB</p>"
// Selectors
const orderQuantityNumber = document.querySelector('.order_quantity_number')
const orderTotalPrice =     document.querySelector('.total_price_num') 
const orderBtnWrp =         document.querySelector('.create_order_btn_wrapper')
const totalSaveDiv =        document.querySelector('.total_save')
const initialTotalPrice =   document.querySelector('.initial_total_price_num')

function orderBtnState(total) {
    total = parseInt(total)
    let state = false
    if (total > 500) {
        let deliveryMethods = document.querySelectorAll('input[name="order_delivery_method"]') 
        if (deliveryMethods.length > 0) {
            for (let method of deliveryMethods) {
                if (method.checked) { state = true  }
            }
        } else {  state = true }
    } 
    if (state == false) {
        orderBtnWrp.classList.add('disabled') 
    } else if (state == true) {
        orderBtnWrp.classList.remove('disabled') 
    }
    console.log(state);
}

// Variables
var   orderItemRemove = undefined

function cartInit() {
    Counter()
    for (let remove of document.querySelectorAll('.order_item__remove')) {
        remove.onclick = () => { RemoveFromCart(remove) }; 
    }
}


function setPromocode(data=null) {
    const couponTotalDiscount = document.querySelector('.coupon_total_discount')
    const couponTotalDiscountSpan = couponTotalDiscount.querySelector('span')
    if (data) {
        couponTotalDiscount.classList.add('active')
        couponTotalDiscountSpan.innerHTML = data + ' RUB'
    } else {
        couponTotalDiscount.classList.remove('active')
        couponTotalDiscountSpan.innerHTML = 'нет'
    }
    
}


function updateOrder(data) {
    if (parseInt(data['quantity']) == 0) {
        window.location.replace("/");
    }
    // Quantity
    if (orderQuantityNumber) { orderQuantityNumber.innerHTML = data['quantity'] }

    // Coupon
    couponFunc = this['setPromocode']
    if (couponFunc != undefined ) {
        couponFunc(data['coupon_discount'])
    }
   
    // Product list
    orderProductsList.innerHTML = nunjucks.renderString(orderProductTpl, data);

    // Total save
    if (data['total_save'] > 0) {
        totalSaveDiv.innerHTML = nunjucks.renderString(totalSaveTpl, {total_save : data['total_save']});
    } else { totalSaveDiv.innerHTML = "" }

    // Order total
    if (data['total_initial']) {
        initialTotalPrice.innerHTML = data['total_initial']
        orderBtnState(data['total_initial'])
    } else {
        initialTotalPrice.innerHTML = data['total']
        orderBtnState(data['total'])
    }
    orderTotalPrice.innerHTML = data['total']

    // Total
    
    cartInit()
}

function updateCartQuantity(counter) {
    let input = counter.querySelector('input')
    AddToCart(input)
}

