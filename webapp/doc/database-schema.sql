--Authors: Duc, Sky

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS authors_books;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS genres_votes;
DROP TABLE IF EXISTS awards;
DROP TABLE IF EXISTS books_awards;
DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books_users;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS ratings;

-- 0, 1, 4, 7, 8, 15, 16, 17, 21, 23, 24, 26, 30
CREATE TABLE books (
    id SERIAL,
    -- series_id int,  (not included for end-to-end assignment)
    title text,
    cover_link text,
    rating_count int,
    review_count int,
    number_of_page int,
    date_published text,
    publisher text,
    isbn13 text,
    settings text,
    characters text,
    amazon_link text,
    descriptions text
);

CREATE TABLE series (
    id SERIAL,
    series text
);

CREATE TABLE authors (
    id SERIAL,
    full_name text,
    birth_place text,
    genre text
);

CREATE TABLE authors_books (
    author_id int,
    book_id int
);

CREATE TABLE genres (
    id SERIAL,
    genre text
);

CREATE TABLE genres_votes (
    book_id int,
    genre_id int,
    vote int
);


CREATE TABLE awards (
    id SERIAL,
    award text
);

CREATE TABLE books_awards (
    book_id int,
    award_id int,
    year int
);

CREATE TABLE recommendations (
    current_book_id int,
    recommended_book_id text
);

CREATE TABLE users (
    username text,
    password_hash int
);

CREATE TABLE books_users (
    book_id int,
    user_id int
);

CREATE TABLE reviews (
    id SERIAL,
    user_id int,
    book_id int,
    content text,
    review_time date
);

CREATE TABLE ratings (
    id SERIAL,
    user_id int,
    book_id int,
    rating int --(1-5)
);

\copy books from 'books.csv' DELIMITER ',' CSV NULL AS ''
