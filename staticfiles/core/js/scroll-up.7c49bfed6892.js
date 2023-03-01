$(document).ready(function () {
  "use strict";

  $(window).scroll(function () {
    // back to top
    let height = $(window).scrollTop();

    // back to top
    if (height > 100) {
      $("#back2Top").fadeIn();
    } else {
      $("#back2Top").fadeOut();
    }
  });

  // Back to top
  $("#back2Top").click(function (event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  });
});
