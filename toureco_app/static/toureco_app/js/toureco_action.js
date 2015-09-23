$(document).ready(function(){
    $('.btn-finish').hide();
    var finish = false;

    $('.limit-select').change(function(e){
        var len = $(this).val().length;

        if (len == 3) {
            if (!finish){
                $('.btn-finish').show('fast');
            }

            $('.btn-finish').on('click', function(){
                $('.limit-select option:not(:selected)').addClass('hide');
                $('.limit-select').attr('size', 9);
                $('.btn-finish').hide('fast');
                finish = true;
            });
        } else {
            $('.btn-finish').hide('fast');
            $('.next-action').hide();
        }
    });
});
