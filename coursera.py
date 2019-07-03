from lxml import html, etree
from random import shuffle
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import time


def get_courses_list(courses_count=5):
    courses_list = []
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    request = requests.get(url).content
    tree = html.fromstring(request)

    for loc in tree.xpath('.//url/loc'):
        url = loc.text
        courses_list.append(url)
    shuffle(courses_list)
    return courses_list[:courses_count]


def get_response(url):
    driver = webdriver.Firefox(executable_path='/home/xatt/Python/devman/geckodriver')
    driver.get(url)
    html = driver.page_source
    return html


def get_start_date(soup):
    try:
        time.sleep(1)
        start_date = soup.find(id='start-date-string').text.replace('Starts ', '')
    except AttributeError:
        start_date = 'Unknown'
    return start_date


def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'itemprop': 'ratingValue'}).text
    except AttributeError:
        rating = 'Unknown'
    return rating


def get_course_info(courses_list):
    course_info = []
    for url in courses_list:
        html = get_response(url)
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.text.split('|')[0]
        language = soup.select_one('.ProductGlance > :last-of-type h4').text
        weaks = len(soup.find(class_='Syllabus').find_all('div', text = re.compile('Week')))
        rating = get_rating(soup)
        start_date = get_start_date(soup)
        course_info.append([title, language, start_date, weaks, rating])
    return course_info


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    courses_list = get_courses_list()
    courses_info = get_course_info(courses_list)
    print(courses_info)
