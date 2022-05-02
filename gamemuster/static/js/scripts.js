window.onload = function () {
    let cards = document.getElementsByClassName('item')
    let sorts = document.getElementsByClassName('sortItem')
    let genres = document.getElementsByClassName('genre')
    let platforms = document.getElementsByClassName('platform')

    for (let i = 0; i < sorts.length; i++) {
        let el = sorts.item(i)
        el.onclick = function () {
            const url = new URL(window.location.href)
            const searchParams = url.searchParams
            const ordering = el.getAttribute('name')

            if (searchParams.has('ordering') && searchParams.get('ordering') === ordering) {
                searchParams.set('order', searchParams.get('order') === 'asc' ? 'desc' : 'asc')
            }
            else if (searchParams.has('ordering') && searchParams.has('order')) {
                searchParams.set('ordering', ordering)
                searchParams.set('order', 'asc')
            }
            else {
                searchParams.append('ordering', ordering)
                searchParams.append('order', 'asc')
            }
            window.location.assign(url)
        }
    }

    for (let i = 0; i < platforms.length; i++) {
        let el = platforms[i]
        el.onclick = function () {
            const url = new URL(window.location.href)
            const searchParams = url.searchParams

            if (searchParams.has('platforms')) {
                searchParams.set('platforms', el.innerText + ',')
            }
            else {
                searchParams.append('platforms', el.innerText + ',')
            }
            window.location.assign(url)
        }
    }

    for (let i = 0; i < genres.length; i++) {
        let el = genres[i]
        el.onclick = function () {
            const url = new URL(window.location.href)
            const searchParams = url.searchParams

            if (searchParams.has('genres')) {
                searchParams.set('genres', el.innerText + ',')
            }
            else {
                searchParams.append('genres', el.innerText + ',')
            }
            window.location.assign(url)
        }
    }


    for (let item in cards) {
        let el = cards[item]
        el.onclick = function () {
            const url = el.getAttribute('url')
            fetch(document.location.origin + url, {
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
            fetch(document.location.origin + url, {
                method: 'POST',
                cache: 'no-cache'
            }).then((result) => {
                if (result.status === 200) {
                    if (el.textContent === 'reMust') {
                        el.textContent = 'UnMust'
                        el.classList.add('bg-danger')
                        el.classList.remove('bg-success')
                    } else {
                        el.textContent = 'reMust'
                        el.classList.remove('bg-danger')
                        el.classList.add('bg-success')
                    }
                }
            })
        }
    }
}

function toPage(n) {
    const url = new URL(window.location.href)
    if (url.searchParams.has('page')) {
        url.searchParams.set('page', n)
    }
    else {
        url.searchParams.append('page', n)
    }
    window.location.assign(url)
}

function filterByName() {
    const url = new URL(window.location.href)
    const gameName = document.getElementById('gameName').name
    if (url.searchParams.has('name')) {
        url.searchParams.set('name', gameName)
    }
    else {
        url.searchParams.append('name', gameName)
    }
    window.location.assign(url)
}
