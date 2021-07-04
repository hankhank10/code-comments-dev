let html_icon_plus = '<i class="far fa-plus-square"></i>'
let html_icon_comment = '<i class="fas fa-star make_red"></i>'

let comment_bar_expanded = false;
let simplemde;
let current_comment_line_id;
let current_comment_id;

function initial_setup() {
    factory_reset_icons()
    simplemde = new SimpleMDE({
        element: $("#comment_input")[0],
        toolbar: [
            'code',
            '|',
            'heading',
            'bold',
            'italic',
            'strikethrough',
            '|',
            'link',
            'image',
            '|',
            'preview',
            'guide',
        ],
        status: false
    });

    $('#create_comment').hide()
    $('#save_comment').hide()
    $('#container_comment_input').hide()

    hljs.highlightAll();
}


function check_comments() {

    factory_reset_icons()

    let gist_id = $('#gist_id').text()

    $.getJSON({
        url: '/api/script_comments/' + gist_id,
        type: 'GET',

        success: function (response) {

            for (item in response) {
                line_id = response[item].line_id
                comment_id = response[item].comment_id

                $('#comment_icon_'+line_id).removeClass('invisible-permanent')
                $('#comment_icon_'+line_id).attr('data-id', comment_id)
                $('#new_comment_clicker_'+line_id).removeClass('faded').addClass('invisible-permanent')
            }

        },
        contentType: 'application/json; charset=utf-8'
    });

}

function factory_reset_icons() {
    $('.new_comment_clicker').html(html_icon_plus)
    $('.new_comment_clicker').addClass('faded').removeClass('invisible-temp').removeClass('invisible-permanent').removeClass('not-faded')

    $('.comment_icon').addClass('invisible-permanent').removeClass('invisible-temp')
    $('.comment_icon').html(html_icon_comment)
}

function comment_bar_expand() {
    $('#comment_bar').addClass('h-250').removeClass('h-50')
    $('#container_comment_input').show()
    comment_bar_expanded = true;
}

function comment_bar_shrink() {
    $('#comment_bar').addClass('h-50').removeClass('h-250')
    simplemde.value('')

    $('#create_comment').hide()
    $('#save_comment').hide()
    $('#container_comment_input').hide()

    $('.new_comment_clicker').removeClass('invisible-temp').addClass('faded').removeClass('not-faded')
    $('.comment_icon').removeClass('invisible-temp')
    comment_bar_expanded = false;
}

function comment_bar_toggle() {
    if (comment_bar_expanded) {
        comment_bar_shrink()
    } else {
        comment_bar_expand()
    }
}

function new_comment_show(line_id) {
    current_comment_line_id = line_id;
    comment_bar_expand();
    $('#delete_comment').hide()
    $('#create_comment').show()

}

function edit_comment_show(comment_id) {
    current_comment_id = comment_id;

    $.getJSON({
        url: '/api/comment?comment_id=' + comment_id,
        type: 'GET',
        success: function (response) {
            simplemde.value(response.comment_content)
        },
        contentType: 'application/json; charset=utf-8'
    });

    comment_bar_expand();
    $('#save_comment').show()
    $('#delete_comment').show()

}

function save_comment(comment_id) {
    $.ajax({
        url: '/api/comment',
        type: 'PUT',
        data: JSON.stringify({
                "comment_id": comment_id,
                "comment_content" : simplemde.value()
        }),
        success: function (response) {
            toastPrimaryAlert("success", "Comment saved")
            check_comments();
            comment_bar_shrink()
        },
        contentType: 'application/json; charset=utf-8'
    });
}

function delete_comment(comment_id) {

    $.ajax({
        url: '/api/comment',
        type: 'DELETE',
        data: JSON.stringify({
                "comment_id": comment_id
        }),
        success: function (response) {
            toastPrimaryAlert("success", "Comment deleted")
            check_comments();
            comment_bar_shrink()
        },
        contentType: 'application/json; charset=utf-8'
    });
}

function create_comment(line_id) {

    $.post({
        url: '/api/comment',
        data: JSON.stringify({
                "line_id": line_id,
                "comment_content" : simplemde.value()
        }),
        success: function (response) {
            toastPrimaryAlert("success", "Comment added")
            check_comments();
            comment_bar_shrink()
        },
        contentType: 'application/json; charset=utf-8'
    });

}

//////////////
// Setup    //
//////////////
initial_setup()
check_comments()

//////////////
// Handlers //
//////////////

// Handle mouseovers
$('.new_comment_clicker').hover(
    function() {
        if (!$(this).hasClass('invisible-temp') && !$(this).hasClass('invisible-permanent')) {$(this).addClass('text-success').removeClass('faded')}
    }, function () {
        if (!$(this).hasClass('invisible-temp') && !$(this).hasClass('invisible-permanent')) {$(this).removeClass('text-success').addClass('faded')}
    }
);

// Handle clicks
//$('#delete_comment').click( function() { delete_comment() })
$('#discard_comment_changes').click( function() { comment_bar_shrink() })

$('#create_comment').click(
    function() {
        create_comment(current_comment_line_id);
    }
)

$('#save_comment').click(
    function() {
        save_comment(current_comment_id);
    }
)

$('#delete_comment_confirm').click(
    function() {
        delete_comment(current_comment_id);
    }
)

$('.new_comment_clicker').click(function() {
    $('.new_comment_clicker').removeClass('faded').addClass('invisible-temp')
    $('.comment_icon').addClass('invisible-temp')
    $(this).removeClass('faded').addClass('not-faded').removeClass('invisible-temp')
    new_comment_show($(this).attr("data-id"))
})

$('.comment_icon').click(function() {
    $('.new_comment_clicker').removeClass('faded').addClass('invisible-temp')
    $('.comment_icon').addClass('invisible-temp')
    $(this).removeClass('invisible-temp')
    edit_comment_show($(this).attr("data-id"))
})

