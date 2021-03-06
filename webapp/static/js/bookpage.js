/*
 * @Author: Tianyi Lu
 * @Description: 
 * @Date: 2021-03-06 03:37:46
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-06 08:18:30
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

function renderBook(id) {
    if (!id) {
        window.location.href = getBaseURL()
    }
    
    var url = getAPIBaseURL() + '/books/' + id;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(book) {
        var listBody = ''
        description = book['description']

        if (!book['cover_link']) {
            book['cover_link'] = getStaticURL() + '/default_book_cover.jpg'
        }

        var imgElement = document.getElementById('book-img');
        if (imgElement) {
            imgElement.innerHTML = '<img class="book-img" src="' + book['cover_link'] + '">';
        }

        listBody += '<h4>'+ book['title']+'</h4>'
                    + '<p>' + book['date_published'] + '</p>'
                    + '<p>' + description + '</p>'
                    + '<h4>' + book['average_rate'] + '</h4>'
                    + '<h4>' + book['rating_count'] + '</h4>'
                    + '<hr/>';

        var bookElement = document.getElementById('book-details');
        if (bookElement) {
            bookElement.innerHTML = listBody;
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

    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString);
    var id = urlParams.get('id')

    renderBook(id)
}