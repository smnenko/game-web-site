window.onload = function () {
    let cards = document.getElementsByClassName('item')
    let sorts = document.getElementsByClassName('sortItem')
    let genres = document.getElementsByClassName('genre')
    let platforms = document.getElementsByClassName('platform')
    let arrowUp = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up" viewBox="0 0 16 16">
                       <path d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z"/>
                   </svg>`
    let arrowDown = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down" viewBox="0 0 16 16">
                         <path d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z"/>
                     </svg>`
    let check = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                     <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                 </svg>`

    for (let i = 0; i < sorts.length; i++) {
        let el = sorts.item(i)
        const url = new URL(window.location.href)
        const searchParams = url.searchParams
        const ordering = el.getAttribute('name')

        if (searchParams.has('ordering') && searchParams.get('ordering') === ordering) {
            searchParams.get('order') === 'asc' ? el.innerHTML += ' ' + arrowDown : el.innerHTML += ' ' + arrowUp
        }
        el.onclick = function () {

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
        const url = new URL(window.location.href)
        const searchParams = url.searchParams

        if (searchParams.has('platforms') && searchParams.get('platforms').split(',').includes(el.textContent))
            el.innerHTML += ' ' + check

        el.onclick = function () {
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
        const url = new URL(window.location.href)
        const searchParams = url.searchParams

        if (searchParams.has('genres') && searchParams.get('genres').split(',').includes(el.textContent))
            el.innerHTML += ' ' + check

        el.onclick = function () {

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

    random_btn = document.getElementById('random_game')
    random_btn.onclick = function () {
        resp = fetch(document.location.origin + '/games/random/', {
            method: 'GET',
            cache: 'no-cache'
        }).then((response) => response.json().then(
            (result) => {
                if (response.status == 200) {
                    window.location.assign(document.location.origin + result.url)
                }
            }
        ))
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
