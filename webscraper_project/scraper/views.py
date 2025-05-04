from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import csv

def index(request):
    return render(request, 'scraper/index.html')

def scrape_books(request):
    url = "http://books.toscrape.com/catalogue/page-1.html"
    response_csv = HttpResponse(content_type='text/csv')
    response_csv['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response_csv)
    writer.writerow(['Title', 'Price', 'Availability'])

    while url:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        books = soup.select('article.product_pod')

        for book in books:
            title = book.h3.a['title']
            price = book.select_one('.price_color').text
            availability = book.select_one('.availability').text.strip()
            writer.writerow([title, price, availability])

        next_btn = soup.select_one('li.next > a')
        if next_btn:
            next_page = next_btn['href']
            url = 'http://books.toscrape.com/catalogue/' + next_page
        else:
            url = None

    return response_csv
