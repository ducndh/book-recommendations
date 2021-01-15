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
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

def get_arguments():
    parser = argparse.ArgumentParser(description='Enter some information to start looking for books')
    parser.add_argument('-t', '--title', type=str, nargs='+',
                        help='print books whose titles contains the argument')
    parser.add_argument('-a', '--author', type=str, nargs='+',
                        help='print authors whose names contains the argument and a list of their books')
    parser.add_argument('-y', '--year', type=str, nargs='+',
                        help='print books published between two year arguments')                    

    args = parser.parse_args()


    return args

def read_file():

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
                if not book in tlist:
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

def get_year(args, books):
    if not args.year:
        return None

    if (len(args.year) % 2) == 1:
        args.year.pop()
    i = 0
    ylist = []
    sortedYears = sorted(args.year)
    while i < (len(args.year) - 1):
        for book in books:
            if book.year >= sortedYears[i] and book.year <= sortedYears[i + 1]:
                ylist.append(book)
        i += 2

    return ylist  
    
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def combine(tlist, adict, ylist):
    tylist = []
    if tlist and ylist:
        tylist = intersection(tlist, ylist)
    elif tlist:
        tylist = tlist
    elif ylist:
        tylist = ylist
    if adict:
        for author, books in adict.items():
            adict[author] = intersection(books, tylist)
        for author in adict.keys():
            print()
            print(author+": ")
            if not adict[author]:
                print( "\t No books matched for this author")
            else:
                for book in adict[author]:
                    print("\t" + str(book))
                
    else:
        for book in tylist:
            print(book)

if __name__ == "__main__":
    args = get_arguments()
    books = read_file()
    tlist = get_title(args, books)
    ylist = get_year(args, books)
    adict = get_author(args, books)
    combine(tlist, adict, ylist)
    
