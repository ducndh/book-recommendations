CREATE TABLE artists (
    artist_id int,
    name text,
    birth_year int,
    death_year int,
    gender text,
    nationality text,
    artist_bio text,
);

CREATE TABLE book (
    id int,
    series_id int,
    title text,
    cover_link text,
    rating_count int,
    review_count int,
    average_rating float,
    number_of_page int,
    date_published date,
    publisher text,
    original_title text,
    isbn int,
    isbn13 int,
    settings text,
    characters text,
    amazon_link text,
    descriptions text,
);

CREATE TABLE series (
    id SERIAL,
    series text,
);

CREATE TABLE authors (
    id SERIAL,
    last_name text,
    first_name text,
    birth_place text,
    genre text,
);

CREATE TABLE authors_books (
    author_id int,
    book_id int,
);

CREATE TABLE genres (
    id SERIAL,
    genre text,
);

CREATE TABLE genres_votes (
    book_id int,
    genre_id int,
    vote int, 
);


CREATE TABLE awards (
    id SERIAL,
    award text,
);

CREATE TABLE books_awards (
    book_id int,
    award_id int,
    year int,
);

CREATE TABLE recommendations (
    current_book_id int,
    recommended_book_id text,
);

CREATE TABLE users (
    user text,
    password_hash int,
);

CREATE TABLE books_users (
    book_id int,
    user_id int,
);

CREATE TABLE reviews (
    id SERIAL,
    user_id int,
    book_id int,
    content text,
    review_time date,
);

CREATE TABLE reviews (
    id SERIAL,
    user_id int,
    book_id int,
    rating int,
    rating_time date,
);
