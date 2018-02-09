/*$(document).ready(function(){
    $(".desc_div").slideUp();
    $(".open_div").click(function(){

        $(this).next(".desc_div").slideToggle("slow").siblings('.desc_div').slideUp();
    });
})
*/

$('.collapse').on('show.bs.collapse', function () {
    $('.collapse.in').collapse('hide');
});