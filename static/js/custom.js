//
//                      |
//    __|  |   |   __|  __|   _ \   __ `__ \
//   (     |   | \__ \  |    (   |  |   |   |
//  \___| \__,_| ____/ \__| \___/  _|  _|  _|
//

if ($('.js-min-fullheight').height() < $(window).height()) {
    $('.js-min-fullheight').height($(window).height());
}
$(window).on('resize', function () {
    if ($('.js-min-fullheight').height() < $(window).height()) {
        $('.js-min-fullheight').height($(window).height());
    }
});

$('.js-fullheight').height($(window).height());
$(window).on('resize', function () {
    $('.js-fullheight').height($(window).height());
});

// $(function() {
//
//   $(".progress").each(function() {
//
//     var value = $(this).attr('data-value');
//     var left = $(this).find('.progress-left .progress-bar');
//     var right = $(this).find('.progress-right .progress-bar');
//
//     if (value > 0) {
//       if (value <= 50) {
//         right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)');
//       } else {
//         right.css('transform', 'rotate(180deg)');
//         left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)');
//       }
//     }
//
//   });
//
//   function percentageToDegrees(percentage) {
//
//     return percentage / 100 * 360;
//
//   }
//
// });


