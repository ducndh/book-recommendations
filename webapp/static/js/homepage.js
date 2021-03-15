/*
 * @Author: Duc, Sky
 * @Description: 
 * @Date: 2021-02-23 20:20:40
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-16 02:45:40
 */

import { getBaseURL, getStaticURL, getAPIBaseURL } from './url.js';
import { renderStars } from './star.js';
import { getSearchResult } from './search.js';

window.onload = initialize;

function renderHeadline(numItems) {
    var url = getAPIBaseURL() + '/books'

    fetch(url, {method: 'get'})
    
    .then((response) => response.json())

    .then(function(books) {
        var listBody = ''

        if (books.length < numItems) {
            numItems = books.length
        }

        for (var k = 0; k < numItems; k++) {
            var book = books[k]

            listBody += '<a class="headline-item" href="'+getBaseURL()+'/book?id='+book['id']+'">'
                      + '<img class="headline-img" src="' + book['cover_link'] + '">'
                      + '</a>'
        }
        
        var headlineElement = document.getElementById('headline');
        if (headlineElement) {
            headlineElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function renderGenres() {
    var url = getAPIBaseURL() + '/genres'

    fetch(url, {method: 'get'})
    
    .then((response) => response.json())

    .then(function(genres) {
        var listBody = ''

        for (var k = 0; k < 10; k++) {
            var genre = genres[k]

            listBody += '<a class="genre-item" href="' + getBaseURL() + '/search?genres=' + genre +'">'
                    //   + '<div class="genre-item">'
                      + '<p>' + genre + '</p>'
                    //   + '</div>'
                      + '</a>'
        }
        
        var genreElement = document.getElementById('genre-content');
        if (genreElement) {
            genreElement.innerHTML = listBody;
        }
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

    renderHeadline(4)
    renderGenres()
    renderBookList('/order_by_rating', 'highly-rated', 4)
    renderBookList('/order_by_date', 'newly-published', 4)
    
}

