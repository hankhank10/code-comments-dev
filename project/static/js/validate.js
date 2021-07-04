let form_is_valid = false;
let password_is_value = false;
let username_available = false

reset_signup_form()

function reset_signup_form() {
    $('#signup_email').val('')
    $('#password1').val('')
    $('#password2').val('')
    $('#label_password_too_short').hide()
    $('#label_passwords_do_not_match').hide()
    form_is_valid = false;

    $('#signup_submit').prop('disabled', true)
    $('.username_feedback').hide()
}

function check_form() {
    form_is_valid = true
    $('#label_password_too_short').hide()
    $('#label_passwords_do_not_match').hide()
    $('#signup_password1').removeClass('is-invalid')
    $('#signup_password2').removeClass('is-invalid')
    $('#signup_submit').prop('disabled', true)

    // Check if all the fields are populated
    if ($('#signup_username').val() == "") { form_is_valid = false }
    if ($('#signup_password1').val() == "") { form_is_valid = false }
    if ($('#signup_password2').val() == "") { form_is_valid = false }

    // If both password fields are completed then check if they match
    if ($('#signup_password1').val() != "" && $('#signup_password2').val() != "") {

        if ($('#signup_password1').val() != $('#signup_password2').val()) {
            form_is_valid = false
            $('#label_passwords_do_not_match').show()
            $('#signup_password1').addClass('is-invalid')
            $('#signup_password2').addClass('is-invalid')
        }
    }

    if (form_is_valid) {
        $('#signup_submit').prop('disabled', false)
    }

}

function check_username() {

    $('#label_username_available_false').hide()
    $('#label_username_available_true').hide()
    $('#label_username_available_checking').show()

    $.getJSON({
        url: '/api/username_available',
        type: 'GET',
        data : {
            username: $('#signup_username').val()
        },

        success: function (response) {

            $('#label_username_available_checking').hide()
            if (response.available) {
                $('#label_username_available_true').show()
                $('#signup_username').removeClass('is-invalid')
            } else {
                $('#label_username_available_false').show()
                $('#signup_username').addClass('is-invalid')
            }

        },
        contentType: 'application/json; charset=utf-8'
    });

}


$('.signup-form-item').blur(function() {
    check_form();
});


$('#signup_username').on('input', function() {

    if ($('#signup_username').val() == "") {
        $('.username_feedback').hide()
    } else {
        check_username()
    }

});