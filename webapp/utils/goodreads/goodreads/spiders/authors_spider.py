'''
Author: Tianyi Lu
Description: 
Date: 2021-03-02 21:40:14
LastEditors: Tianyi Lu
LastEditTime: 2021-03-02 23:57:36
'''

import scrapy
import csv
import os

parent_dir = '/home/skylu/Desktop/Carleton/CS257/cs257/webapp'

def nextURL():
    with open(parent_dir + '/static/goodreads_books.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = []
        for row in csv_reader:
            rows.append(row[6])

        return list(set(rows[1:]))
       

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    total = 0;
    
    def start_requests(self):

        for url in nextURL():
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        full_name = response.css('h1.authorName span::text').get()
        cover_link = response.css('div.leftContainer a img::attr(src)').get()
        try:
            birth_date = response.css('div.dataItem[itemprop="birthDate"]::text').get().strip(' \n\t')
        except:
            birth_date = None

        about = response.css('div.aboutAuthorInfo span *').get()

        with open(parent_dir + '/static/authors1.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([self.total, full_name, cover_link, birth_date, about])
            self.total += 1


        

