$(document).ready(function () {
  gsap.registerPlugin(ScrollTrigger);

  // Animación listado de posts del blog.
  gsap.utils.toArray(".intro-post").forEach(function (e) {
    gsap.from(e, {
      duration: 1,
      ease: "power2.inOut",
      stagger: 0.2,
      opacity: 0,
      scale: 0,
      scrollTrigger: e,
      // onComplete: () => console.log(e)
    });
  });
});
