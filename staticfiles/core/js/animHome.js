$(document).ready(function(){
  gsap.registerPlugin(ScrollTrigger);

  // Animación Intro
  let t1 = gsap.timeline({
    scrollTrigger: {
      trigger: "#intro-home"
    }
  });
  t1.from("#intro-home-image", { x: 200, opacity: 0, duration: 1.5 }).from(
    ".anim1",
    { y: -50, opacity: 0, duration: 1, stagger: 0.2 },
    "-=1"
  );

  // Animación Tablero
  let t2 = gsap.timeline({
    scrollTrigger: {
      trigger: "#tablero-ajedrez"
    }
  });
  t2.from("#tablero-ajedrez-image", { scale: 0, opacity: 0, duration: 0.5 })
    .from(".anim3", { y: 100, opacity: 0, duration: 0.5 })
    .from(".anim2", { x: -100, opacity: 0, duration: 0.5 });

  // Animación Texto
  gsap.to(".mytext", {
    scrollTrigger: "#intro-news",
    duration: 1,
    text: "Últimas publicaciones",
    delay: 1
  });

  // Animación Noticias
  let t3 = gsap.timeline({
    scrollTrigger: {
      trigger: "#intro-news",
      start: "top center"
    }
  });
  if (window.matchMedia("(min-width: 768px)").matches) {
    t3.from(".anim4", { x: -200, opacity: 0, duration: 1, stagger: 0.2, ease: "power2.inOut" });
  } else {
    t3.from(".anim4", { y: -200, opacity: 0, duration: 1, stagger: 1 });
  }

  // Parallax move Mouse
  // document.addEventListener("mousemove", parallax);
  // function parallax(event) {
  //   this.querySelectorAll(".parallax-wrap span").forEach(shift => {
  //     const position = shift.getAttribute("value");
  //     const x = (window.innerWidth - event.pageX * position) / 90;
  //     const y = (window.innerHeight - event.pageY * position) / 90;

  //     shift.style.transform = `translateX(${x}px) translateY(${y}px)`;
  //   });
  // }

  // apply parallax effect to any element with a data-speed attribute
  gsap.to("[data-speed]", {
    // y: (i, el) => (1 - parseFloat(el.getAttribute("data-speed"))) * ScrollTrigger.maxScroll(window),
    y: (i, target) => -ScrollTrigger.maxScroll(window) * target.dataset.speed,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-wrap",
      start: "top center",
      end: "max",
      invalidateOnRefresh: true,
      scrub: 0
    }
  });

  // Massive image (parallax horizontal)
  // gsap.set(".massiveImage", {backgroundImage: `url(https://source.unsplash.com/random/${innerWidth * 3}x${innerHeight})`})

  //gsap.to(".massiveImage", {
  //  xPercent: -100,
  //  x: () => innerWidth,
  //  ease: "none",
  //  scrollTrigger: {
  //    trigger: ".massiveImage",
  //    start: "top top",
  //    end: () => innerWidth * 3,
  //    scrub: true,
  //    pin: true,
  //    invalidateOnRefresh: true,
  //    anticipatePin: 1
  //  }
  //});

  // Parallax Background Image
  gsap.to(".section-3-1219", {
    backgroundPosition: "50% 100%",
    ease: "none",
    scrollTrigger: {
      trigger: ".section-3-1219",
      start: "top bottom",
      end: "bottom top",
      scrub: true
    }
  });
});
