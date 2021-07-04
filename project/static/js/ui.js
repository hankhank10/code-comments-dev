//let light_style_sheet = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/a11y-light.min.css";
let highlightjs_light = "/static/css/a11y-light-custom.css";
let highlightjs_dark = "/static/css/a11y-dark-custom.css";

//let simplemde_light = "https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css"
//let simplemde_dark = "https://cdn.rawgit.com/xcatliu/simplemde-theme-dark/master/dist/simplemde-theme-dark.min.css\n"

let simplemde_light = "/static/css/simplemde_light.css"
let simplemde_dark = "/static/css/simplemde_dark.css"


window.onload = function() {
    sync_highlight_js()
}

function swapStyleSheet(element_id, sheet) {
    document.getElementById(element_id).setAttribute('href',sheet);
}

function toggle_dark() {
    halfmoon.toggleDarkMode()
    sync_highlight_js()
}

function sync_highlight_js () {
    if (halfmoon.darkModeOn) {
        swapStyleSheet('highlight_css_sheet', highlightjs_dark)
        swapStyleSheet('simplemde_css_sheet', simplemde_dark)

    } else {
        swapStyleSheet('highlight_css_sheet',highlightjs_light)
        swapStyleSheet('simplemde_css_sheet', simplemde_light)
    }
}

