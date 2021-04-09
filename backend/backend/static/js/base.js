document.getElementsByClassName('filter-button')[0].onclick = function() {
    let el = document.getElementsByClassName('filter-button')[0];
    el.style.display == 'flex' ? el.style.display = 'none' : el.style.display = 'flex';
}
