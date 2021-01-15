'''
Author: Tianyi Lu, Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 09:19:27
'''

import argparse
import csv

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

class Book()
    


def read_file(args):
//row[0] = title //
//row[1] = year //
//row[2] = author //

    with open('books.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Number of matches:  {line_count}')

def get_title(args):
    pass

def get_author(args):
    pass

def get_year(args):
    pass

def combine(tlist, alist, ylist):
    pass

if __name__ == "__main__":
    pass
