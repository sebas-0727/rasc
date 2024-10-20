var swiper = new Swiper(".mySwiper", {
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    loop:true,
    slidesPerView: "auto",
    coverflowEffect: {
        rotate: 50,
        stretch: 0,
        depth: 150,
        modifier: 2.5,
        slideShadows: true,
    },
    autoplay:{

        delay:3000,
        disableOnInteraction:false,
    }

});