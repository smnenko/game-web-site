document.getElementById('filter-button').onclick = function() {
    let el = document.getElementById('filter');
    el.style.width == '50px' ? el.style.width = '300px' : el.style.width = '50px';
    el.style.height == '50px' ? el.style.height = '300px' : el.style.height = '50px';
    el.style.background-color = 'pink';
}

document.getElementById('slider').oninput = function getVar() {
    let value = document.getElementById('filter-rating-scroll-value');
    let slider = document.getElementById('slider');

    value.innerHTML = slider.value;
}

let elm = document.querySelector('input');
let container = elm.parentNode;
let values = elm.getAttribute('data-values').split(' ');

values.forEach(function (value, i, values) {
    let rangePart = elm.cloneNode();
})