from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

print("----------------Huffington Post News Page -------")
testsource = requests.get("https://www.huffingtonpost.ca/news/good-news/", headers={'User-Agent': 'Mozilla/5.0'}).text


soup = BSoup(testsource, 'html.parser')
huff_news = []

allTheArticles = soup.findAll('div', class_='card')
firstEightArticles = allTheArticles[:6]

for huffArticle in firstEightArticles:

	headline = huffArticle.find('h2').text

	summary = huffArticle.find('div', class_='card__description').text

	image_src = str(huffArticle.find('img')['src']).split(" ")[-1]
	url = str(huffArticle.find('a')['href']).split(" ")[-1]

	new_headline = Headline()
	new_headline.title = headline
	new_headline.url = url
	new_headline.image = image_src
	huff_news.append(new_headline)

good_news = []

source = requests.get("https://www.goodnewsnetwork.org/category/news/").text

soup1 = BSoup(source, 'html.parser')
allGoodNewsArticles = soup1.findAll('div', class_='td_module_3 td_module_wrap td-animation-stack')

firstFive_GoodNewsArticles = allGoodNewsArticles[1:6]

checkPodcastString = "Boost Your Mood"


lengthOfList = 0
x = 5
y = 0
while lengthOfList <= 4:
	for goodNewsArticle in firstFive_GoodNewsArticles:
		headline = goodNewsArticle.find('h3').text
		image_src = str(goodNewsArticle.find('img')['src']).split(" ")[-1]
		url = str(goodNewsArticle.find('a')['href']).split(" ")[-1]


		if checkPodcastString in headline:
			break

		new_headline = Headline()
		new_headline.title = headline
		new_headline.url = url
		new_headline.image = image_src
		good_news.append(new_headline)

	lengthOfList = len(good_news)
	if len(good_news) <= 4:
		y = 5 - len(good_news)

	firstFive_GoodNewsArticles = allGoodNewsArticles[x:(x+y)]
	x = x + y

#Getting news from Positive News
print("----------------Positive News Page -------")
source = requests.get("https://www.positive.news/articles/").text


soup = BSoup(source, 'html.parser')
pos_news = []

thirdEightArticles = allTheArticles[12:13]

for posArticle in soup.findAll('div', class_='column card'):

	headline = posArticle.find('div', class_='card__content').a.text

	summary = posArticle.find('div', class_='card__content').span.text

	image_src = str(posArticle.find('img')['src']).split(" ")[-1]

	url = str(posArticle.find('a')['href']).split(" ")[-1]

	new_headline = Headline()
	new_headline.title = headline
	new_headline.url = url
	new_headline.image = image_src
	pos_news.append(new_headline)

for huffArticle in thirdEightArticles:

	headline = huffArticle.find('h2').text

	summary = huffArticle.find('div', class_='card__description').text

	image_src = str(huffArticle.find('img')['src']).split(" ")[-1]

	url = str(huffArticle.find('a')['href']).split(" ")[-1]

	new_headline = Headline()
	new_headline.title = headline
	new_headline.url = url
	new_headline.image = image_src
	pos_news.append(new_headline)

def index(req):
    return render(req, 'news/home.html', {'huff_news':huff_news, 'pos_news': pos_news, 'good_news':good_news})

