document.addEventListener("DOMContentLoaded", function(){
    manage_theme_switcher()
})

function manage_theme_switcher(){
    let theme_switch = document.getElementById('theme_switch');

    theme_switch.addEventListener('change', function(){
        console.log(document.body.classList.contains('light'))
        if (document.body.classList.contains('light')) {
            // dark mode time
            document.body.classList.remove('light');
            document.body.style["--bg1"] = null;
            document.body.style["--bg2"] = null;
        } else {
            // light mode time
            document.body.classList.add('light');
            document.body.style["--bg1"] = "#DEDEDE";
            document.body.style["--bg2"] = "#FDFDFD";
        }
    })
}