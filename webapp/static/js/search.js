/*
 * @Author: Tianyi Lu
 * @Description: 
 * @Date: 2021-03-06 04:55:15
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-06 07:39:13
 */

window.onload = initialize;

function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port
    return baseURL
}

function getAPIBaseURL() {
    return getBaseURL() + '/api';
}

function getStaticURL() {
    return getBaseURL() + '/static';
}

function renderStars(average_rate) {
    result = ''
    numStars = parseInt(average_rate)
    for (var k = 0; k < numStars; k++) {
        result += '<span class="fa fa-star checked"></span>'
    }

    for (var k = 0; k < (5-numStars); k++) {
        result += '<span class="fa fa-star"></span>'
    }

    return result   
}
function toURLParams(title, setting, character, genre, isbn13) {
    url = ''
    if (title) {
        url += '&title=' + title
    }
    if (setting) {
        url += '&setting=' + setting
    }
    if (character) {
        url += '&character=' + character
    }
    if (genre) {
        url += '&genres=' + genre
    }
    if (isbn13) {
        url += '&isbn13=' + isbn13
    }

    return url
}

function renderSearchResult(title, setting, character, genre, isbn13) {
    var url = getAPIBaseURL() + '/books/search?'
    
    url += toURLParams(title, setting, character, genre, isbn13)
    fetch(url, {method: 'get'})
    
    .then((response) => response.json())

    .then(function(books) {
        var listBody = '<h3>Search Result</h3>'

        for (var k = 0; k < 10; k++) {
            var book = books[k]
            var description
            var title

            if (book['description'] && book['description'].length > 600) {
                description = book['description'].slice(0, 600) + ' ...(more)'
            } else {
                description = book['description']
            }

            // if (book['title'].length > 100) {
            //     title = book['title'].slice(0, 100) + ' ...'
            // } else {
            title = book['title']
            // }

            if (!book['cover_link']) {
                book['cover_link'] = getStaticURL() + '/default_book_cover.jpg'
            }

            listBody += '<div class="book-item">'
                    + '<img class="book-img" src="' + book['cover_link'] + '">'
                    + '<div class="book-text">'
                    + '<h4>' + title + '</h4>'
                    + '<p>'
                    + renderStars(book['average_rate'])
                    + ' ' + book['average_rate'] + ' (' + book['rating_count'] + ')'
                    + '</p>'
                    + '<p>' + description + '<p>'
                    + '<div class="book-date">' + book['date_published'] + '</div>'
                    + '</div>'
                    + '</div>';
        }

        var bookListElement = document.getElementById('search-results');
        if (bookListElement) {
            bookListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getResultAndRender(event) {
    event.preventDefault()
    var title = document.getElementById("title-input").value;
    var setting = document.getElementById("setting-input").value;
    var character = document.getElementById("character-input").value;
    var genre = document.getElementById("genres-input").value
    var isbn13 = document.getElementById("isbn13-input").value

    url = getBaseURL() + '/search?'
    url += toURLParams(title, setting, character, genre, isbn13)
    window.location.href = url
}

function getSearchResult(event) {
    event.preventDefault()
    var searchKey = document.getElementById("basic-search").value;
    url = getBaseURL() + '/search?title=' + searchKey;
    window.location.href = url;
}

function initialize() {
    var searchForm = document.getElementById('search-form')
    searchForm.addEventListener('submit', getSearchResult)

    var form = document.getElementById("advance-form")
    form.addEventListener('submit', getResultAndRender)
    
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString);
    renderSearchResult(urlParams.get('title'), urlParams.get('setting'), 
                       urlParams.get('character'), urlParams.get('genres'),
                       urlParams.get('isbn13'))

}


