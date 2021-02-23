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
    var artwork_title = document.getElementById('artwork-title')
    if (artwork_title) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "artwork_title=" + artwork_title.value;
    }
    var min_year = document.getElementById('artwork-minyear')
    if (min_year) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_year=" + min_year.value;
    }
    var max_year = document.getElementById('artist-maxyear')
    if (max_year) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_year=" + max_year.value;
    }
    var min_height = document.getElementById('minheight')
    if (min_height) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_height=" + min_height.value;
    }
    var max_height = document.getElementById('maxheight')
    if (max_height) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_height=" + max_height.value;
    }
    var min_width = document.getElementById('minwidth')
    if (min_width) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_width=" + min_width.value;
    }
    var max_width = document.getElementById('maxwidth')
    if (max_width) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_width=" + max_width.value;
    }
    var classification = document.getElementById('classification')
    if (classification) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "classification=" + classification.value;
    }
    var sort_by = document.getElementById('sort-artworks')
    if (sort_by) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "sort_by=" + sort_by.value;
    var url = getAPIBaseURL() + '/books/' + parameters;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        var listBody = '';
        for (var k = 0; k < books.length; k++) {
            var book = books[k];
            listBody += '<li>' + book['name']
                      + ', ' + book['birth_year']
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

