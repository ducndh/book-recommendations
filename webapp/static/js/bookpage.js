window.onload = initialize;

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function getStaticURL() {
    var staticURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/static';
    return staticURL
}

function renderBook(endpoint, elementId) {
    var url = getAPIBaseURL() + '/books' + endpoint;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        var book = books[0]
        var listBody = ''
            if (book['description'].length > 600) {
                var description = book['description'].slice(0, 600) + ' ...(more)'
            } else {
                description = book['description']
            }

            if (!book['cover_link']) {
                book['cover_link'] = getStaticURL() + '/default_book_cover.jpg'
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
                      + '<h4>' + book['average_rate'] + '</h4>'
                      + '<h4>' + book['rating_count'] + '</h4>'
                      + '</div>'
                      + '</div>'
                      + '</li>'
                      + '<hr/>';

        var bookElement = document.getElementById(elementId);
        if (bookElement) {
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

    renderBookList('/240213', 'book')
}