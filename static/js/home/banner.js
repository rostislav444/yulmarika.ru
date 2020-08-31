var swiperBanner = document.querySelector('.swiper-container')


if (swiperBanner) {
  var mySwiper = new Swiper('.swiper-container', {
    loop: true,
    autoplay: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: true,
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
  swiperBanner.onmouseover = swiperBanner.onmouseout = handler;
}
