'''
Author: Tianyi Lu, Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 10:13:53
'''

import argparse
import csv

class Book():
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author

    def __repr__(self):
        return ", ".join([self.title, self.year, self.author])

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
    tlist = []
    for arg in args.title:
        for book in books:
            if arg in book.title:
                tlist.append(book)
    return set(tlist)                

        

def get_author(args, books):
    pass

def get_year(args):
    pass

def combine(tlist, alist, ylist):
    pass

if __name__ == "__main__":
    args = get_arguments()
    books = read_file()
    for book in books:
        
        print(book)
    
