/*
 * @Author: Tianyi Lu
 * @Description: 
 * @Date: 2021-03-06 04:55:15
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-16 02:54:10
 */

import { getBaseURL, getStaticURL, getAPIBaseURL } from './url.js';
import { renderStars } from './star.js';

window.onload = initialize;

export function getSearchResult(event) {
    event.preventDefault()
    var searchKey = document.getElementById("basic-search").value;
    var url = getBaseURL() + '/search?title=' + searchKey;
    window.location.href = url;
}

function toURLParams(title, setting, character, genre, isbn13) {
    var url = ''
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

function renderSearchResult(title, setting, character, genre, isbn13, num) {
    var url = getAPIBaseURL() + '/books/search?'
    
    url += toURLParams(title, setting, character, genre, isbn13)
    fetch(url, {method: 'get'})
    
    .then((response) => response.json())

    .then(function(books) {
        var listBody = ''
        
        if (books.length == 0) {
            listBody = '<h3>No Result</h3>'
                     + '<p>Please change your search content.</p>'
        } else {
            listBody = '<h3>Search Result for: '

            if (title) {
                var titleInput = document.getElementById('title-input')
                titleInput.value = title
                listBody += '<i>title:'+title+', </i>'
            }
            
            if (setting) {
                var settingInput = document.getElementById('setting-input')
                settingInput.value = setting
                listBody += '<i>setting:'+setting+', </i>'
            }
            
            if (character) {
                var characterInput = document.getElementById('character-input')
                characterInput.value = character
                listBody += '<i>character:'+character+', </i>'
            }

            if (genre) {
                var genreInput = document.getElementById('genres-input')
                genreInput.value = genre
                listBody += '<i>genre:'+genre+', </i>'
            }

            if (isbn13) {
                var isbn13Input = document.getElementById('isbn13-input')
                isbn13Input.value = isbn13
                listBody += '<i>isbn13:'+isbn13+', </i>'
            }

            listBody += '</h3>'

            var noMore = false

            for (var k = 0; k < num; k++) {
                var book = books[k]
                var description

                if (!book) {
                    noMore = true;
                    break;
                }
                
                if (book['description'] && book['description'].length > 600) {
                    description = book['description'].slice(0, 600) + ' ...(more)'
                } else if (book['description'] == null) {
                    description = 'No description'
                } else {
                    description = book['description']
                }

                var bookTitle = book['title']

                if (!book['cover_link']) {
                    book['cover_link'] = getStaticURL() + '/default_book_cover.jpg'
                }

                listBody += '<a class="book-item" href="' + getBaseURL() + '/book?id='+book['id'] + '">'
                        + '<img class="book-img" src="' + book['cover_link'] + '">'
                        + '<div class="book-text">'
                        + '<h4>' + bookTitle + '</h4>'
                        + '<p>'
                        + renderStars(book['average_rate'])
                        + ' ' + book['average_rate'] + ' (' + book['rating_count'] + ')'
                        + '</p>'
                        + '<p>' + description + '<p>'
                        + '<div class="book-date">' + book['date_published'] + '</div>'
                        + '</div>'
                        + '</a>';
            }
            
            if (!noMore) {
                listBody += '<button id="more">more</button>'
            }
        }

        var bookListElement = document.getElementById('search-results');

        
        if (bookListElement) {
            bookListElement.innerHTML = listBody;

            if (books.length != 0) {
                var moreButton = document.getElementById("more");
    
                moreButton.addEventListener('click', function(){
                    renderSearchResult(title, setting, character, genre, isbn13, num+5);
                });
            }
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

    var url = getBaseURL() + '/search?'
    url += toURLParams(title, setting, character, genre, isbn13)
    window.location.href = url
}

function renderMoreResult() {
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString);
    renderSearchResult(urlParams.get('title'), urlParams.get('setting'), 
                       urlParams.get('character'), urlParams.get('genres'),
                       urlParams.get('isbn13'), 20)
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
                       urlParams.get('isbn13'), 10)
               
}


