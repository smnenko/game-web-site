window.onload = function () {
    let classes = document.getElementsByClassName('item')
    for (let item in classes) {
        let el = classes[item]
        el.onclick = function () {
            const url = el.getAttribute('url')
            fetch('http://localhost:8000' + url, {
                method: 'POST',
                cache: 'no-cache'
            }).then((result) => {
                if (result.status === 200) {
                    el.textContent === 'Must' ? el.textContent = 'UnMust' : el.textContent = 'Must'
                }
            })
        }
    }
}
