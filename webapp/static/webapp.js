/*
 * @Author: Duc, Sky
 * @Description: 
 * @Date: 2021-02-23 20:20:40
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-02-23 22:36:56
 */
/*
 * webapp.js
 * Jeff Ondich
 * 6 November 2020
 *
 * A little bit of Javascript for the tiny web app sample for CS257.
 */

window.onload = initialize;

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function initialize() {

    var url = getAPIBaseURL() + '/books';
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        var listBody = '';
        for (var k = 0; k < books.length; k++) {
            var book = books[k];
            var description

            if (book['description'].length > 600) {
                description = book['description'].slice(0, 600) + ' ...(more)'
            } else {
                description = book['description']
            }

            listBody += '<li class="book">'
                      + '<div class="book-cover">'
                      + '<img class="book-img" src="' + book['cover_link'] + '">'
                      + '</div>'
                      + '<div class="book-intro">'
                      + '<div class="intro-content">'
                      + '<h4>'+ book['title']+'</h4>'
                      + '<p>' + book['date_published'] + '</p>'
                      + '<p>' + description + '</p>'
                      + '</div>'
                      + '</div>'
                      + '<div class="book-rating">'
                      + '<div class="rating-content">'
                      + '<h4>' + '#Ratings' + '</h4>'
                      + '<h4>' + book['rating_count'] + '</h4>'
                      + '</div>'
                      + '</div>'
                      + '</li>'
                      + '<hr/>';
        }

        var bookListElement = document.getElementById('book-list');
        if (bookListElement) {
            bookListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

