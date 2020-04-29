#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import urllib.request
import time

source = './springer-has-released-65-machine-learning-and-data-books-for-free.html'
target = './books'


try:
    if os.path.exists(target):
        backup = target + ".backup_" + str(time.time_ns())
        os.rename(target, backup)
    os.mkdir(target)
except OSError:
    print("Creation of the directory %s failed" % target)
    sys.exit(1)

with open(source) as file:
    source_html = file.read()

soup = BeautifulSoup(source_html, "html.parser")
soup.findAll('strong', class_="hl")
all_books = soup.findAll('strong')

n = 1
total = len(all_books)
for book in all_books:
    title = book.next_element
    authors = title.next_element.next_element
    if not authors.find('a'):
        continue

    url = authors.next_element.a['href']

    response = requests.get(url)
    book_soup = BeautifulSoup(response.text, "html.parser")
    books = book_soup.findAll(title="Download this book in PDF format")

    book_path = books[0]['href']
    o = urlparse(url)
    base = o.scheme + "://" + o.netloc
    book_url = base + book_path
    author = authors.split(",")[0]

    book_filename = os.path.join(target, title + " by " + author + ".pdf")
    print("[%2d/%d] Downloading %s ..." % (n, total, book_filename))
    n += 1
    urllib.request.urlretrieve(book_url, book_filename)
    time.sleep(1)
