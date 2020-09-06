from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

from .models import Search


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def index(request):
    return render(request, 'craigsearch/base.html')


def search(request):
    search = Search()
    search_text = request.POST['search_str']
    search.search_text = search_text
    search.save()
    
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search_text))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')

    post_lists = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_lists:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
           post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    context = {
        'search_text': search_text,
        'final_postings': final_postings,
    }

    return render(request, 'craigsearch/craigsearch_search.html', context)