$(function() {
   $('.saveForm').click(function() {
        let sand  = parseFloat($('#sand').val());
        let silt  = parseFloat($('#silt').val());
        let clay  = parseFloat($('#clay').val());
        if ((sand + clay + silt) !==  100){
             $('#error-message').text("Make the sum of %sand, %silt and %clay equal to 100")
             $('#error').fadeIn();
            return false
        }
        $('#formCalculate').submit();
   })

    $('.input').change(function() {
        let sand  = parseFloat($('#sand').val() || 0);
        let silt  = parseFloat($('#silt').val() || 0);
        let clay  = parseFloat($('#clay').val() || 0);
        percent = parseFloat(sand + clay + silt)
        if (percent === 100) {
            $('#progress').removeClass('bg-danger');
            $('#progress').addClass('bg-success');
        }else{
            $('#progress').removeClass('bg-success');
            $('#progress').addClass('bg-danger');
        }

        $('#progress').css('width', percent+'%');
        $('#progress').text(percent+'%');
   })

   $('.input').trigger('change');
})


