--Authors: Duc, Sky

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS books_authors;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS genres_votes;
DROP TABLE IF EXISTS awards;
DROP TABLE IF EXISTS books_awards;
DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books_users;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS ratings;

-- 0, 1, 4, 7, 8, 9, 15, 16, 17, 21, 23, 24, 26, 30
CREATE TABLE books (
    id SERIAL,
    title text,
    cover_link text,
    series_id int,
    rating_count int,
    review_count int,
    average_rate float,
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
    cover_link text,
    birth_place text,
    about text
);

CREATE TABLE books_authors (
    book_id int,
    author_id int
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
    recommended_book_id int
);

-- CREATE TABLE users (
--     username text,
--     password_hash int
-- );

-- CREATE TABLE books_users (
--     book_id int,
--     user_id int
-- );

-- CREATE TABLE reviews (
--     id SERIAL,
--     user_id int,
--     book_id int,
--     content text,
--     review_time date
-- );

-- CREATE TABLE ratings (
--     id SERIAL,
--     user_id int,
--     book_id int,
--     rating int --(1-5)
-- );

\copy books from '../static/books.csv' DELIMITER ',' CSV NULL AS ''
\copy series from '../static/series.csv' DELIMITER ',' CSV NULL AS ''
\copy authors from '../static/authors.csv' DELIMITER ',' CSV NULL AS ''
\copy books_authors from '../static/books_authors.csv' DELIMITER ',' CSV NULL AS ''
\copy genres from '../static/genres.csv' DELIMITER ',' CSV NULL AS ''
\copy genres_votes from '../static/genres_votes.csv' DELIMITER ',' CSV NULL AS ''
\copy awards from '../static/awards.csv' DELIMITER ',' CSV NULL AS ''
\copy books_awards from '../static/books_awards.csv' DELIMITER ',' CSV NULL AS ''
\copy recommendations from '../static/recommendations.csv' DELIMITER ',' CSV NULL AS ''

