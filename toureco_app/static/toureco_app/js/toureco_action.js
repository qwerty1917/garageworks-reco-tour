$(document).ready(function(){
    var finish = false;

    $('.limit-select').change(function(e){
        var len = 0;

        if ($(this).val())
            var len = $(this).val().length;
        
        if (len == 3) {
            if (!finish)
                $('.btn-finish').show('fast');

            $('.btn-finish').on('click', function(){
                $('.limit-select option:not(:selected)').addClass('hide');
                $('.limit-select').attr('size', 4);
                $('.btn-finish').hide('fast');

                finish = true;

                $('.limit-select').find('option:not(:selected)').remove();
                $('.choice-title').html('Rank choices!');
                $('.next-action').show('fast');
                $('.btn-up').show('fast');

                $('.limit-select').removeAttr('multiple');
            });
        } else {
            $('.btn-finish').hide('fast');

            if (!finish)
                $('.next-action').hide();
        }
    });

    $('.limit-select').change();

    $('.btn-up').on('click', function(){
        var $op = $('.limit-select option:selected'),
            $this = $(this);

        if($op.length){
            $op.first().prev().before($op);
        }
    });
});
