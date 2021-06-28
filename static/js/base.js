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
                    if (el.textContent === 'UnMust')
                        el.textContent = 'Must'
                    else
                        el.textContent = 'UnMust'
                }
            })
        }
    }

    let musts = document.getElementsByClassName('must')
    for (let must in musts) {
        let el = musts[must]
        el.onclick = function () {
            const url = el.getAttribute('url')
            fetch('http://localhost:8000' + url, {
                method: 'POST',
                cache: 'no-cache'
            }).then((result) => {
                if (result.status === 200) {
                    if (el.textContent === 'reMust') {
                        el.textContent = 'UnMust'
                        el.classList.add('bg-danger')
                        el.classList.remove('bg-success')
                    }
                    else {
                        el.textContent = 'reMust'
                        el.classList.remove('bg-danger')
                        el.classList.add('bg-success')
                    }
                }
            })
        }
    }
}
