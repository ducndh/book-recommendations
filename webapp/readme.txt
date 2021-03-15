AUTHORS: Duc Nguyen and Sky Lu

DATA: The data contains books information that is scraped from Goodreads, include authors, genres, settings, characters and other information

The data is from Kaggle.com with link https://www.kaggle.com/austinreese/goodreads-books
Additional information about the authors were crawled down from the Goodreads website: https://www.goodreads.com/

FEATURES CURRENTLY WORKING:
- Explore books on homepage (random books, highly rated books and newly published books).
- Find books by popular genres on homepage.
- Search for books by title, character, setting, genre, isbn13.
- Expand search result by clicking "more" button at the bottom.
- Individual book information page, containing detailed information about the book, the author and other recommended books.

FEATURES NOT YET WORKING:
- Login and bookshelf functions are abandoned due to the difficulty of implement login.
- Not enough author information was available to crawl down to make independent author page.

Note:
- The crawler implemented by using "scrapy" is in the utils folder.
- The data.sql has been sent via Slack (identical to the one in first draft).
- Advance search options can stick in user's view when scrolling.
- Some books' titles or descriptions are unknown characters due to the original dataset.
- Some books' titles or descriptions may contain inappropriate elements. 
  We are unable to eliminate all of them due to the size of the dataset. 
