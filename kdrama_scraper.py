from bs4 import BeautifulSoup as bs
import requests
import sys

#ACCESS SEARCH PAGE AND DETERMINE WHETHER THERE ARE VALID RESULTS

def getTop(soup):
    search_results = soup.find('div', class_='col-lg-8 col-md-8')
    boxes = search_results.find_all('div', class_='box')
    ranks = []

    for box in boxes:
        try:
            rank = box.find('div', class_='ranking pull-right').text.strip()[1:]
            ranks.append(int(rank))
        
        except:
            ranks.append(999999)
            pass

    min_rank = ranks.index(min(ranks))
    return boxes[min_rank]

#FIND TOP RANK OF SEARCH RESULTS
def getTopPage(soup):
    highest_rank = getTop(soup)
    href = highest_rank.find('a').get('href')
    main_url = 'https://mydramalist.com/' + href
    return main_url

def getImg(drama_page):
    cover = drama_page.find('div', class_='film-cover')
    img = cover.find('img', class_='img-responsive')
    src = img.get('src')
    return src

#ACCESS DRAMA PAGE OF FIRST RESULT IF THERE
def getstuff(drama):
    # GET URL AND USER INPUT
    url = 'https://mydramalist.com/search?q='

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
    print(f'\nSynopsis: \n{synopsis}\n')

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()
    print(rating)

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []
    
    print('\nCast:')
    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)
        print(member_name)

    return synopsis, rating, members, img, title


    #Genres
    # genre_list = drama_info.find('div', class_='list-item p-a-0 show-genres')
    # genres = genre_list.find_all('a', class_='text-primary') 

    #Reviews