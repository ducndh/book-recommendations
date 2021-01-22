'''
Author: Tianyi Lu, Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-22 15:55:14
'''

import argparse
import csv

class Book():
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author

    def __repr__(self):
        return ', '.join([self.title, self.year, self.author])
    
    # for 'in' and '==' to work with Book class
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

def get_arguments():
    """
    Get argument from command line
    :return: args object
    """
    parser = argparse.ArgumentParser(prog="python3 books.py",
                                     description='Search books based on different methods.')
    # Accessed by args.title
    parser.add_argument('-t', '--title', type=str, nargs='+',
                        help='print books whose titles contains the argument')
    # Accessed by args.author
    parser.add_argument('-a', '--author', type=str, nargs='+',
                        help='print authors whose names contains the argument and a list of their books')
    # Accessed by args.year
    parser.add_argument('-y', '--year', type=int, nargs='+',
                        help='print books published between two year arguments')                    

    args = parser.parse_args()


    return args

def load_file():
    """
    Load books from books.csv
    :return: A list of book objects
    """
    books = []
    with open('books.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            book = Book(row[0], row[1], row[2])
            books.append(book)
            
    return books

def get_books_by_title(args, books):
    """
    Get books whose titles contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects whose title matches the arguments.
    """
    if not args.title:
        return None

    title_book_list = []
    for arg in args.title:
        for book in books:
            if arg.lower() in book.title.lower():
                if not book in title_book_list:
                    title_book_list.append(book)
    return title_book_list              
        

def get_books_by_author(args, books):
    """
    Get books whose author name contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A dictionary with matched authors' names as key and a list of their
             book objects as value.
    """
    if not args.author:
        return None

    author_book_dict = {}
    # Create a key value pair for every author that matches the arguments
    for arg in args.author:
        for book in books:
            if arg.lower() in book.author.lower():
                if not book.author in author_book_dict.keys():
                    author_book_dict[book.author] = []

    # Fill in the books written by every author in the dictionary
    for book in books:
        if book.author in author_book_dict.keys():
            author_book_dict[book.author].append(book)

    
    return author_book_dict

def get_books_by_year(args, books):
    """
    Get books published between two year arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects published between two year arguments
    """
    if not args.year:
        return None

    # If an odd number of year arguments are entered, pop out the last one.
    if (len(args.year) % 2) == 1:
        args.year.pop()
        
    i = 0
    year_book_list = []
    sortedYears = sorted(args.year)
    while i < (len(args.year) - 1):
        for book in books:
            if int(book.year) >= sortedYears[i] and int(book.year) <= sortedYears[i + 1]:
                if not book in year_book_list:
                    year_book_list.append(book)
        i += 2

    return year_book_list
    
def get_intersect_list(lst1, lst2):
    """
    Find the intersection of two lists
    :param lst1: List One
    :param lst2: List Two
    :return: A list of intersect elements in the two lists
    """
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def combine_print_results(title_book_list, author_book_dict, year_book_list):
    """
    Combine the results from get_title, get_year, and get_author. Print out the
    formated results
    :param title_book_list: A list of book objects from get_title
    :param author_book_dict: A dictionary of author and book objects from get_author
    :param year_book_list: A list of book objects from get_year
    """
    # Intersection list of title_book_list and year_book_list
    title_year_list = []

    only_author_book_dict = False

    # If both title and year arguments appeared in the command line input
    if (title_book_list is not None) and (year_book_list is not None):
        title_year_list = get_intersect_list(title_book_list, year_book_list)

    # If only the title argument appeared in the command line input
    elif title_book_list:
        title_year_list = title_book_list

    # If only the year argument appeared in the command line input
    elif year_book_list:
        title_year_list = year_book_list

    # If only the author argument appeared in the command line input
    else:
        only_author_book_dict = True

    if author_book_dict:
        for author, books in author_book_dict.items():
            if not only_author_book_dict:
                author_book_dict[author] = get_intersect_list(books, title_year_list)
                
        print_dict_result(author_book_dict)
                
    else:
        print_list_result(title_year_list)

def print_dict_result(author_book_dict):
    """
    Arrange and print a dictionary of authors and their books
    :param author_book_dict: A dictionary of authors books to print
    """
    for author in author_book_dict.keys():
        print()
        print(author+": ")
        if not author_book_dict[author]:
            print( "\t(No book matches)")
        else:
            for book in author_book_dict[author]:
                print("\t" + str(book))


def print_list_result(book_list):
    """
    Arrange and print a book list
    :param book_list: a list of books to print
    """
    print("\n%d books found\n" % len(book_list))
    for i, book in enumerate(book_list):
        print(str(i+1)+". "+str(book))

def main():
    args = get_arguments()
    books = load_file()
    title_book_list = get_books_by_title(args, books)
    year_book_list = get_books_by_year(args, books)
    author_book_dict = get_books_by_author(args, books)
    combine_print_results(title_book_list, author_book_dict, year_book_list)

if __name__ == "__main__":
    main()
    