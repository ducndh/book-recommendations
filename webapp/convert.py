'''
Author: Tianyi Lu
Description: Converting goodreads.csv to small csvs we need.
Date: 2021-02-23 18:23:11
LastEditors: Tianyi Lu
LastEditTime: 2021-02-23 19:30:26
'''
import csv
def read_csv(filename):

    rows = []
    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row[16] = date_converter(row[16].split())
                rows.append(row)

    except Exception as e:
        print(e)
    
    return rows[1:]

def write_from_goodreads(filename, position_list, rows):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in rows:
            row_content = [row[x] for x in position_list]
            csv_writer.writerow(row_content)

def date_converter(date_list):
    if (len(date_list) == 0):
        return date_list
    elif (len(date_list) == 1):
        return '-'.join([date_list[0], '01', '01'])
    elif (len(date_list) == 3):
        return '-'.join([date_list[2], 
                         map_month_to_number(date_list[0]), 
                         map_date_to_number(date_list[1])])  
    else:
        return ''

def map_month_to_number(input_string):
    month_dict = {'january': '01',
                  'februrary': '02',
                  'march': '03',
                  'april': '04',
                  'may': '05',
                  'june': '06',
                  'july': '07',
                  'august': '08',
                  'september': '09',
                  'october': '10',
                  'november': '11',
                  'december': '12'}

    return month_dict.get(input_string.lower(), '01')

def map_date_to_number(input_string):
    number = input_string[:-2]
    return '0'+number if len(number) == 1 else number


if __name__ == "__main__":
    goodreads_rows = read_csv('static/csv/goodreads_books.csv')
    write_from_goodreads('static/csv/books.csv', [0, 1, 4, 7, 8, 15, 16, 17, 21, 23, 24, 26, 30], goodreads_rows)