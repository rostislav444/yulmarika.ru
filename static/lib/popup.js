// PopUp
const PopupWrapper = document.querySelector('.popup__wrapper')
const PopupInner =   PopupWrapper.querySelector('.popup__inner')

function popupClose(selector) {
    if (selector == undefined) {
        PopupWrapper.classList.remove('active')
    } else {
        document.querySelector(selector).classList.remove('active')
    }
}

function popupOpen(selector) {
    if (selector == undefined) {
        PopupWrapper.classList.add('active')
    } else {
        document.querySelector(selector).classList.add('active')
    }
   
}