$(document).ready(function(){

    init();

    $('.option-item').on('click', function(){
        var select = $('.choice');

        var parent_ul = $(this).parent();
        var is_multiple = hasattr(parent_ul, 'multiple');

        var is_selected = $(this).hasClass('option-item-selected');
        var value = $(this).data('value');

        if (is_selected) {
            $(this).removeClass('option-item-selected');
            select.find('option[value="' + value + '"]').prop('selected', false);
        } else {
            if (!is_multiple){
                $('.option-item').removeClass('option-item-selected');
                select.find('option').prop('selected', false);
            }
            $(this).addClass('option-item-selected');
            select.find('option[value="' + value + '"]').prop('selected', true);
        }

        select.change();
    });

    $('.limit-select').change(function(e){
        var len = 0;

        if ($(this).val())
            var len = $(this).val().length;

        if (len == 3) {
            if (!finish)
                $('.btn-finish').show('fast');

            $('.btn-finish').unbind().click(function(){
                finish = true;

                $('.btn-finish').hide('fast');
                $('.choice-title').html('Rank choices!');
                $('.next-action').show('fast');
                $('.btn-up').show('fast');

                $('.limit-select').find('option:not(:selected)').remove();
                $('.select-list').find('.option-item:not(.option-item-selected)').remove()
                $('.select-list').find('.option-item').removeClass('option-item-selected');
                $('.select-list').removeAttr('multiple');
            });
        } else {
            $('.btn-finish').hide('fast');

            if (!finish)
                $('.next-action').hide();
        }
    });

    $('.btn-up').on('click', function(){
        var $item = $('.select-list').find('.option-item-selected');
        var $op = $('.limit-select').find('option:selected');

        if($item.length){
            $item.first().prev().before($item);
            $op.first().prev().before($op);
        }
    });

    initTrigger();
});

function init(){
    finish = false;
}

function initTrigger(){
    $('.choice').change();
}

function hasattr(element, attr){
    var hasAttr = false;
    var attribute = element.attr(attr);

    if (typeof attribute !== typeof undefined && attribute !== false) {
        hasAttr = true;
    }

    return hasAttr;
}
