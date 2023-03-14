from sqlalchemy.sql import text as sa_text
from BD.alchemy import db_session
import requests
from bs4 import BeautifulSoup
from BD import Model_db

def england_parser():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://www.premierleague.com/tables'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    club_content = soup.findAll("tr", {"data-compseason": "489"})

    # так как данные тянутся с таблицы всегда актуальные, нет смысла обновлять базу, проще удалить данные и записать по новой
    # так точно не будет дублирований
    db_session.execute(sa_text('TRUNCATE TABLE england_table').execution_options(autocommit=True))

    # вытягивание данных и запись в базу
    for i in club_content:
        position = i.find("span", {"class": "value"}).text
        club_name = i.find("span", {"class": "long"}).text
        club_site = i.find("a")['href']
        tmp = club_site.replace('overview', 'stats')
        club_stat_url = 'https://www.premierleague.com' + tmp
        game = i.findAll("td")[3].text
        won = i.findAll("td")[4].text
        drawn = i.findAll("td")[5].text
        lost = i.findAll("td")[6].text
        goals_for = i.findAll("td", {"class": "hideSmall"})[0].text
        goals_against = i.findAll("td", {"class": "hideSmall"})[1].text
        points = i.find("td", {"class": "points"}).text

        insert_query = Model_db.England(position=position, club_name=club_name, club_stat_url=club_stat_url,
                                         game=game, won=won, drawn=drawn, lost=lost, goals_for=goals_for,
                                        goals_against=goals_against, points=points)
        db_session.add(insert_query)
        db_session.commit()
        db_session.close()

def german_parser():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://www.bundesliga.com/en/bundesliga/table'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    club_content = soup.findAll("tr", {"class": "ng-star-inserted"})
    # так как данные тянутся с таблицы всегда актуальные, нет смысла обновлять базу, проще удалить данные и записать по новой
    # так точно не будет дублирований
    db_session.execute(sa_text('TRUNCATE TABLE germany_table').execution_options(autocommit=True))

    for i in club_content:
        position = i.find("td", {"class": "rank"}).text
        club_name = i.find("span", {"class": "d-none d-sm-inline-block"}).text
        game = i.find("td", {"class": "matches"}).text
        won = i.find("td", {"class": "wins"}).text
        drawn = i.find("td", {"class": "draws"}).text
        lost = i.find("td", {"class": "losses"}).text
        goals = i.find("td", {"class": "goals"}).text
        goals_for = str(goals).split(':')[0]
        goals_against = str(goals).split(':')[-1]
        points = i.find("td", {"class": "pts"}).text
        tmp_site = i.find("a", {"class": "logolink"})['href']
        club_site = 'https://www.bundesliga.com' + tmp_site

        insert_query = Model_db.Germany(position=position, club_name=club_name, club_stat_url=club_site,
                                        game=game, won=won, drawn=drawn, lost=lost, goals_for=goals_for,
                                        goals_against=goals_against, points=points)
        db_session.add(insert_query)
        db_session.commit()
        db_session.close()
        # print(club_site)
        # print('///////////////////////////////////////')
# england_parser()
# german_parser()
