document.addEventListener("DOMContentLoaded", function(){
    manage_theme_switcher()
})

function manage_theme_switcher(){
    let theme_switch = document.getElementById('theme_switch');

    theme_switch.addEventListener('change', function(){
        console.log(document.body.classList.contains('light'))
        if (document.body.classList.contains('light')) {
            document.body.classList.remove('light');
        } else {
            document.body.classList.add('light');
        }
    })
}