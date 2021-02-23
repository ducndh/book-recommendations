/*
 * webapp.js
 * Jeff Ondich
 * 6 November 2020
 *
 * A little bit of Javascript for the tiny web app sample for CS257.
 */

window.onload = initialize;

function initialize() {
    var element = document.getElementById('search_button');
    if (element) {
        element.onclick = onCatsButton;
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onSearchButton() {
    var parameters = ""
    var basic_search = document.getElementById('basic_search')
    if (basic_search) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "title=" + basic_search.value;
    var url = getAPIBaseURL() + '/books/' + parameters;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        var listBody = '';
        for (var k = 0; k < books.length; k++) {
            var book = books[k];
            listBody += '<li>' + book['title']
                      + ', ' + book['cover_link']
                      + '-' + book['death_year']
                      + ', ' + book['description'];
                      + '</li>\n';
        }

        var bookListElement = document.getElementById('book_list');
        if (booklListElement) {
            bookListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

