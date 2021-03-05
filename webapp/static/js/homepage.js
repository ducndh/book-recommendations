/*
 * @Author: Duc, Sky
 * @Description: 
 * @Date: 2021-02-23 20:20:40
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-06 02:03:01
 */

window.onload = initialize;

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function getStaticURL() {
    var staticURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/static';
    return staticURL
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

function renderBookList(endpoint, elementId, numItems) {
    var url = getAPIBaseURL() + '/books' + endpoint;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        var listBody = ''

        if (books.length < numItems) {
            numItems = books.length
        }

        for (var k = 0; k < numItems; k++) {
            var book = books[k]
            var description
            var title

            if (book['description'].length > 100) {
                description = book['description'].slice(0, 100) + ' ...(more)'
            } else {
                description = book['description']
            }

            if (book['title'].length > 50) {
                title = book['title'].slice(0, 50) + ' ...'
            } else {
                title = book['title']
            }

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

        var bookListElement = document.getElementById(elementId);
        if (bookListElement) {
            bookListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function getSearchResult() {
    var searchKey = document.getElementById("basic-search").value
    alert("key:" + searchKey)
}

function initialize() {

    var searchForm = document.getElementById('search-form')
    searchForm.addEventListener('submit', getSearchResult)

    renderBookList('/order_by_rating', 'highly-rated', 4)
    renderBookList('/order_by_date', 'newly-published', 4)
    
}

