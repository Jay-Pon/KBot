from bs4 import BeautifulSoup as bs
import requests
import sys

# GET URL AND USER INPUT
url = 'https://mydramalist.com/search?q='

#search_query = input("Drama name: ").replace(" ", "+")
search_query = input('Drama name: ').lower()
page = requests.get(url + search_query)
soup = bs(page.text, 'html.parser')

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

#ACCESS DRAMA PAGE OF FIRST RESULT IF THERE
main_url = getTopPage(soup)
drama_page = bs(requests.get(main_url).text, 'html.parser')

#SCRAPE RELEVANT DATA
#Rating, Cast, Description
drama_info = drama_page.find('div', class_='col-sm-8')

#show synopsis
synopsis = drama_info.find('div', class_='show-synopsis').text.strip()
print(f'\nSynopsis: \n{synopsis}\n')

#Rating
rating = drama_info.find('div', class_='hfs').text.strip()
print(rating)

  
# #Cast failed method but could prove useful in the future
# #cast_url = main_url + '/cast'
# #cast_page = requests.get(cast_url)   
# cast_info = bs(cast_page.text, 'html.parser')
# all_cast = cast_info.find_all('ul', class_='list no-border p-b clear')
# main_cast = all_cast[3]
# cast_members = main_cast.find_all('li', class_='list-item col-sm-6')               
# print('\nMain Cast:')
# for member in cast_members:
#     name = member.find('a', class_='text-primary').text.strip()
#     print(name)

#cast
cast_info = drama_page.find('div', class_='p-a-sm')
cast_list = cast_info.find('ul', class_='list no-border p-b')
cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
print('\nCast:')
for member in cast_members:
    member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
    member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
    print(member_name)


#Genres
# genre_list = drama_info.find('div', class_='list-item p-a-0 show-genres')
# genres = genre_list.find_all('a', class_='text-primary') 

#Reviews