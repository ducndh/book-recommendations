'''
Author: Tianyi Lu
Description: 
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 09:19:27
'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
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
