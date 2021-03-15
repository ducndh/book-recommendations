/*
 * @Author: Tianyi Lu
 * @Description: 
 * @Date: 2021-03-06 03:37:46
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-16 04:31:59
 */

import { getBaseURL, getStaticURL, getAPIBaseURL } from './url.js';
import { getSearchResult } from './search.js';
import { renderStars } from './star.js'

window.onload = initialize;


function renderBook(id) {
    if (!id) {
        window.location.href = getBaseURL()
    }
    
    var url = getAPIBaseURL() + '/books/' + id;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(book) {
        var listBody = ''
        var description = book['description']

        if (!book['cover_link']) {
            book['cover_link'] = getStaticURL() + '/default_book_cover.jpg'
        }

        var imgElement = document.getElementById('img');
        if (imgElement) {
            imgElement.innerHTML = '<img class="img" src="' + book['cover_link'] + '">';
        }


        listBody += '<h4>'+ book['title']+'</h4>'
                    + '<p><b>Published Date</b>: ' + book['date_published'] + '</p>'
                    + '<p>' + description + '</p>'
                    + '<p><b>Average Rating</b>: ' + renderStars(book['average_rate']) + book['average_rate'] + '</p>'
                    + '<p><b>Number of Ratings</b>: ' + book['rating_count'] + '</p>'
                    + '<hr/>';

        var bookElement = document.getElementById('book-info');
        if (bookElement) {
            bookElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function renderAuthor(book_id) {
    var url = getAPIBaseURL() + '/books/author/' + book_id;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(author) {
        var htmlBody = '<img class="author-img" src="' + author['cover_link'] + '">'
                     + '<h4 class="author-name">' + author['full_name'] + '</h4>'
        var authorElement = document.getElementById('author-info');
        authorElement.innerHTML = htmlBody
    })

    .catch(function(error) {
        console.log(error);
    });

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

            if (book['description'] && book['description'].length > 100) {
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

            listBody += '<a class="book-item" href="'+getBaseURL()+'/book?id='+book['id']+'">'
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
                      + '</a>';
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

function initialize() {

    var searchForm = document.getElementById('search-form')
    searchForm.addEventListener('submit', getSearchResult)

    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString);
    var id = urlParams.get('id')

    renderBook(id)
    renderAuthor(id)
    renderBookList('/recommendation/'+id, 'recommendations', 4)
}