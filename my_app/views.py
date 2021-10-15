import requests
from requests.compat import quote_plus
from django.shortcuts import render
from django.shortcuts import render
from .models import Search
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
def home(request):
    return render(request,'base.html')

def new_search(request):
    
    search  = request.POST.get('search')
    models.Search.objects.create(search=search)
    #print(quote_plus(search))
    final_url  = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #print (final_url)
    response = requests.get(final_url)

    data = response.text
    soup = BeautifulSoup(data,features = 'html.parser')
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li',{'class':'result-row'})
    post_title = post_listings[0].find(class_ = 'result-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_ = 'result-price').text
    
    print (post_title)
    print (post_price)
    print (post_url)
    #print (soup)
    #print (data)
    context = {
        'search' : search
    }
    return render(request,'my_app/new_search.html',context)