var swiperBanner = document.querySelector('.swiper-container')


if (swiperBanner) {
  var mySwiper = new Swiper('.swiper-container', {
    loop: true,
    autoplay: true,
    autoplay: {
      delay: 5000,
    },
    pagination: {
      el: '.swiper-pagination',
    },
    navigation: {
      nextEl: '.home-banner-next',
      prevEl: '.home-banner-prev',
    },
  })
  
  function handler(event) {
    if (event.type == 'mouseover') {
      mySwiper.autoplay.stop();
    }
    if (event.type == 'mouseout') {
      mySwiper.autoplay.start();
    }
  }
 

  var mediaQueryMatch = window.matchMedia('(max-width: 960px)');
  function screenChange(e) {
    if (e.matches) {
      swiperBanner.removeEventListener('mouseover', handler)
      swiperBanner.removeEventListener('mouseout', handler)
    } else {
      swiperBanner.addEventListener('mouseover', handler)
      swiperBanner.addEventListener('mouseout', handler)
    }
  }

  if (mediaQueryMatch.matches == false) {
    swiperBanner.addEventListener('mouseover', handler)
    swiperBanner.addEventListener('mouseout', handler)
  }
  
  mediaQueryMatch.addListener(screenChange)
  
}
