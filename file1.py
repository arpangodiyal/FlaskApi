from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask_restful import Resource, Api

url = 'https://www.billboard.com/charts/hot-100'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

lis = list()

allSongs = soup.findAll("div", {"class":"chart-list-item"})
no1 = soup.find("div", {"class":"chart-number-one__title"}).text.strip()
no1artist = soup.find("div",{"class" : "chart-number-one__artist"}).a.text.strip()
# print(no1)
# print(no1artist)
# print()

dicto = {"Rank":1, "SongName":no1, "Artist":no1artist, "LyricsUrl":''}
lis.append(dicto)

#print(allSongs[1])

# name = allSongs[0].find("div", {"class":"chart-list-item__title"}).span.text.strip()
# artist = song.find("div", {"class":"chart-list-item__artist"}).a.text.strip()
# lyrics_url = song.find("div", {"class":"chart-list-item__lyrics"}).a["href"]


for song in allSongs:
    name = song["data-artist"]
    artist = song["data-title"]
    rank = song["data-rank"]
    lyrics_url = ''

    if song.find("div", {"class":"chart-list-item__lyrics"}) != None:
        lyrics_url = song.find("div", {"class":"chart-list-item__lyrics"}).a["href"]

    # print(rank)
    # print(name)
    # print(artist)
    # print(lyrics_url)
    # print()
    dicto = {"Rank":rank, "SongName":name, "Artist":artist, "LyricsUrl":lyrics_url}
    lis.append(dicto)

#print(lis)

app = Flask(__name__)
api = Api(app)

class Hot100(Resource):
    def get(self):
        return lis

api.add_resource(Hot100, '/')

if __name__ == '__main__':
    app.run(debug=True)
