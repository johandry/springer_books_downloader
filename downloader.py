#!/usr/bin/env python3
# coding: utf-8

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import urllib.request
import time

file_name = './springer-has-released-65-machine-learning-and-data-books-for-free.html'
with open(file_name) as file:
    source = file.read()

soup = BeautifulSoup(source, "html.parser")
soup.findAll('strong', class_="hl")
for book in soup.findAll('strong'):
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

    book_filename = "./books/" + title + " by " + author + ".pdf"
    print("Downloading %s ..." % book_filename)
    urllib.request.urlretrieve(book_url, book_filename)
    time.sleep(1)
