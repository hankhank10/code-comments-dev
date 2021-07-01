let html_icon_plus = '<i class="far fa-plus-square"></i>'
let comment_bar_expanded = false;
let simplemde;
let current_comment_line_id;

function initial_setup() {
    refresh_comment_clickers()
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
            '|',
            {
                name: "custom",
                action: function customFunction(editor){
                    window.alert("Hi!")
                },
                className: "fas fa-save make_red",
                title: "Custom Button",
            }
        ]
    });

    $('#container_comment_input').hide()

    hljs.highlightAll();
}

function refresh_comment_clickers() {
    $('.new_comment_clicker').show()
    $('.new_comment_clicker').html(html_icon_plus)
    $('.new_comment_clicker').addClass('faded')
}

function comment_bar_expand() {
    $('#comment_bar').addClass('h-250').removeClass('h-50')
    $('#container_comment_input').show()
    comment_bar_expanded = true;
}

function comment_bar_shrink() {
    $('#comment_bar').addClass('h-50').removeClass('h-250')
    simplemde.value('')
    $('#container_comment_input').hide()
    $('.new_comment_clicker').removeClass('invisible-temp').addClass('faded').removeClass('not-faded')
    comment_bar_expanded = false;
}

function comment_bar_toggle() {
    if (comment_bar_expanded) {
        comment_bar_shrink()
    } else {
        comment_bar_expand()
    }
}

function new_comment(line_number) {
    comment_bar_expand()
}

//////////////
// Setup    //
//////////////
initial_setup()

//////////////
// Handlers //
//////////////

// Handle mouseovers
$('.new_comment_clicker').hover(
    function() {
        if (!$(this).hasClass('invisible-temp')) {$(this).addClass('text-success').removeClass('faded')}
    }, function () {
        if (!$(this).hasClass('invisible-temp')) {$(this).removeClass('text-success').addClass('faded')}
    }
);

// Handle clicks
$('#comment_bar').dblclick( function () {comment_bar_toggle()} )
$('#delete_comment').click( function() {comment_bar_shrink()})

$('.new_comment_clicker').click(function() {
    $('.new_comment_clicker').removeClass('faded').addClass('invisible-temp')
    $(this).removeClass('faded').addClass('not-faded').removeClass('invisible-temp')
    new_comment()
})