from bs4 import BeautifulSoup as bs
import requests
import sys
import random

#ACCESS SEARCH PAGE AND DETERMINE WHETHER THERE ARE VALID RESULTS

def getTop(soup):
    search_results = soup.find('div', class_='col-lg-8 col-md-8')
    boxes = search_results.find_all('div', class_='box')
    ranks = []

    for box in boxes:
        try:
            rank = box.find('div', class_='ranking pull-right').text.strip()[1:]
            classification = box.find('span', class_='text-muted').text.strip().split()
            
            if classification[0] == 'Korean' and classification[1] == 'Drama':
                ranks.append(int(rank))
            else:
                ranks.append(999999)
        
        except:
            ranks.append(999999)
            pass

    min_rank = ranks.index(min(ranks))
    return boxes[min_rank]

#FIND A RANDOM DRAMA PAGE
def getRandom(soup):
    search_results = soup.find('div', class_='col-lg-8 col-md-8')
    boxes = search_results.find_all('div', class_='box')
    random_number = random.randint(0, 19)

    return boxes[random_number]

#FIND TOP RANK OF SEARCH RESULTS
def getTopPage(soup):
    highest_rank = getTop(soup)
    href = highest_rank.find('a').get('href')

    main_url = 'https://mydramalist.com/' + href
    return main_url

#ACCESS DRAMA PAGE OF FIRST RESULT IF THERE
def getRandomPage(soup):
    random_box = getRandom(soup)
    href = random_box.find('a').get('href')
    main_url = 'https://mydramalist.com/' + href
    print(main_url)
    return main_url

#GET COVER IMAGE FROM DRAMA
def getImg(drama_page):
    cover = drama_page.find('div', class_='film-cover')
    img = cover.find('img', class_='img-responsive')
    src = img.get('src')
    return src

#ACCESS DRAMA PAGE OF FIRST RESULT IF THERE
def getStuff(drama,  url = 'https://mydramalist.com/search?q='):
    # GET URL AND USER INPUT

    #search_query = input("Drama name: ").replace(" ", "+")
    search_query = drama.lower()
    page = requests.get(url + search_query)
    soup = bs(page.text, 'html.parser')

    main_url = getTopPage(soup)
    drama_page = bs(requests.get(main_url).text, 'html.parser')

    #SCRAPE RELEVANT DATA
    #Rating, Cast, Description, image
    img = getImg(drama_page)

    drama_info = drama_page.find('div', class_='col-sm-8')
    title = drama_page.find('h1', class_='film-title').text

    #show synopsis
    synopsis = drama_info.find('div', class_='show-synopsis').text.strip()

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()

    #genres
    genre_area = drama_info.find('li', class_='show-genres')
    genres = [genre.text for genre in genre_area.find_all('a', class_='text-primary')]

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []

    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)

    return synopsis, rating, members, img, title, genres

def getSuggest():

    # GET URL AND USER INPUT
    url = 'https://mydramalist.com/shows/top'

    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    random_page = getRandomPage(soup)
    drama_page = bs(requests.get(random_page).text, 'html.parser')

    #SCRAPE RELEVANT DATA
    #Rating, Cast, Description, image
    img = getImg(drama_page)

    drama_info = drama_page.find('div', class_='col-sm-8')
    title = drama_page.find('h1', class_='film-title').text

    #show synopsis
    synopsis = drama_info.find('div', class_='show-synopsis').text.strip()
    print(f'\nSynopsis: \n{synopsis}\n')

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()
    print(rating)

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []
    
    #genres
    genre_area = drama_info.find('li', class_='show-genres')
    genres = [genre.text for genre in genre_area.find_all('a', class_='text-primary')]

    print('\nCast:')
    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)
        print(member_name)

    return synopsis, rating, members, img, title, genres
    #Genres
    # genre_list = drama_info.find('div', class_='list-item p-a-0 show-genres')
    # genres = genre_list.find_all('a', class_='text-primary') 

    #Reviews

def getRecommend(genre):
    genre = [g.lower() for g in genre.split()]
    genres = {"action" : "1", "comedy" : "17", "drama" : "25", "law" : "18", "romance" : "19", "sci-fi" : "27", "crime" : "21", "medical" : "30", "mystery" : "11", "tragedy" : "39"}
    url = 'https://mydramalist.com/search?adv=titles&ty=68&ge={list_genres}&st=3&so=top'
    genre_string = ""
    for g in genre:
        genre_string += genres[g] + ","
    url = url.format(list_genres = genre_string)

    page = requests.get(url)
    soup = bs(page.text, 'html.parser')

    main_url = getTopPage(soup)
    drama_page = bs(requests.get(main_url).text, 'html.parser')

    #SCRAPE RELEVANT DATA
    #Rating, Cast, Description, image
    img = getImg(drama_page)

    drama_info = drama_page.find('div', class_='col-sm-8')
    title = drama_page.find('h1', class_='film-title').text

    #show synopsis
    synopsis = drama_info.find('div', class_='show-synopsis').text.strip()

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()

    #genres
    genre_area = drama_info.find('li', class_='show-genres')
    genres = [genre.text for genre in genre_area.find_all('a', class_='text-primary')]

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []

    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)

    return synopsis, rating, members, img, title, genres