'''
Author: Tianyi Lu, Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 10:49:11
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

def get_arguments():
    parser = argparse.ArgumentParser(description='Enter some information to start looking for books')
    parser.add_argument('-t', '--title', type=str, nargs='+',
                        help='print books whose titles contains the argument')
    parser.add_argument('-a', '--author', type=str, nargs='+',
                        help='print authors whose names contains the argument and a list of their books')
    parser.add_argument('-y', '--year', type=str, nargs='+',
                        help='print books published between two year arguments')                    

    args = parser.parse_args()

    print(args.title)
    print(args.author)
    print(args.year)

    return args

def read_file():
    #row[0] = title
    #row[1] = year
    #row[2] = author

    books = []
    with open('books.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            book = Book(row[0], row[1], row[2])
            books.append(book)
            
    return books

def get_title(args, books):
    if not args.title:
        return None

    tlist = []
    for arg in args.title:
        for book in books:
            if arg.lower() in book.title.lower():
                titles = [book.title for book in tlist]
                if not book.title in titles:
                    tlist.append(book)
    return tlist              
        

def get_author(args, books):
    if not args.author:
        return None

    adict = {}
    for arg in args.author:
        for book in books:
            if arg.lower() in book.author.lower():
                if not book.author in adict.keys():
                    adict[book.author] = []

    for book in books:
        if book.author in adict.keys():
            titles = [b.title for b in adict[book.author]]
            if not book.title in titles:
                adict[book.author].append(book)
    return adict

def get_year(args):
    if not args.year:
        ylist = None

    if (len(args.author) % 2) == 1:
        args.author.pop()

    i = 0
    while i < (len(args.year) - 1):
        for book in books:
            book.year.lower():
                authors = [book.author for book in alist]
                if not book.author in authors:
                    alist.append(book)
    return alist  

def combine(tlist, alist, ylist):
    pass

if __name__ == "__main__":
    args = get_arguments()
    books = read_file()
    adict = get_author(args, books)
    for author in adict.keys():
        print(author+": ")
        for book in adict[author]:
            print(book)
    
