var productGalery = document.querySelector('.product__galery')
var productgalerySlides = productGalery.querySelectorAll('.slide')
const body =  document.querySelector('body')

const sliderGalery = new Swiper('.galery', {
    loop: true,
    spaceBetween: 2,
    pagination: {
        el: '.swiper-pagination',
    },
    navigation: {
    nextEl: '.home-banner-next',
    prevEl: '.home-banner-prev',
    },
})

// THUMBS
var thumbs = productGalery.querySelectorAll('.thumb')
for (let i = 0; i < thumbs.length; i++) {
    let el = thumbs[i];
    el.onclick = () => {
        sliderGalery.slideTo(i + 1);
    }
}

// SET ACTIVE THUMB
function setThumbActive(index) {
    for (let i = 0; i < thumbs.length; i++) {
    let el = thumbs[i];
        if (i == index) {
            el.classList.add('active')
        } else {
            el.classList.remove('active')
        }
    }
}
function slideScrollCenter() {
    for (let slide of productGalery.querySelectorAll('.slide')) {
        let img = slide.querySelector('img')
        slide.scrollTop = -img.offsetHeight / 2 + slide.offsetHeight
        slide.scrollLeft = img.offsetHeight / 2 - slide.offsetHeight / 2
    }
}

sliderGalery.on('slideChange', function () {
    playInitial()
    setThumbActive(sliderGalery.realIndex)
    slideScrollCenter()
}); 
setThumbActive(sliderGalery.realIndex)





// FULLSCREEN
const productGalerySlider = productGalery.querySelector('.product__galery__slider')


function OpenFullScreen() {
    for (let slide of productGalery.querySelectorAll('.slide')) {
        slide.classList.add('swiper-no-swiping')
    }
    body.style.overflowY = 'hidden'
    productGalerySlider.classList.add('fullscreen')
    sliderGalery.update()
    slideScrollCenter()
}
function CloseFullScreen() {
    for (let slide of productGalery.querySelectorAll('.slide')) {
        slide.classList.remove('swiper-no-swiping')
    }
    body.style.overflowY = 'auto'
    productGalerySlider.classList.remove('fullscreen')
    sliderGalery.update()
}


for (let slide of document.querySelectorAll('.product_slider_image')) {
    slide.onclick = () => {
        if (productGalerySlider.classList.contains('fullscreen') == false) { 
            OpenFullScreen() 
        } else { 
            CloseFullScreen()
        }
    }
}
const fullscreenClose = productGalery.querySelector('.close')
fullscreenClose.onclick = () => { CloseFullScreen() }