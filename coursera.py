from lxml import html, etree
from random import shuffle
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import time
from openpyxl import Workbook
from os import path
import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description='Данные о курсах на Курсере.')
    parser.add_argument(
        'geckodriver',
        type=str,
        help='Введите путь к скаченному geckodriver.'
    )
    parser.add_argument(
        '-b',
        '--browser',
        type=int,
        default=0,
        help='Если используете Chrome, то введите 1 (если Firefox, то ничего не вводите)'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=os.getcwd(),
        help='Введите путь для сохранения xlsx-файла.'
    )
    parser.add_argument(
        '-c',
        '--count', 
        type=int,
        default=20,
        help='Введите количество курсов.'
    )
    args = parser.parse_args()
    return args


def get_courses_list(courses_count=0):
    courses_list = []
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    request = requests.get(url).content
    tree = html.fromstring(request)

    for loc in tree.xpath('.//url/loc'):
        url = loc.text
        courses_list.append(url)
    shuffle(courses_list)
    return courses_list[:courses_count]


def get_response_firefox(url, driverpath):
    driver = webdriver.Firefox(executable_path='/home/xatt/Python/devman/geckodriver')
    driver.get(url)
    html = driver.page_source
    return html


def get_response_chrome(url, driverpath):
    driver = webdriver.Chrome(executable_path='/home/xatt/Python/devman/geckodriver')
    driver.get(url)
    html = driver.page_source
    return html


def get_start_date(soup):
    try:
        time4load = 1
        time.sleep(time4load)
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


def get_weaks(soup):
    try:
        weaks = len(soup.find(class_='Syllabus').find_all('div', text = re.compile('Week')))
    except AttributeError:
        weaks = 'Unknown'
    return weaks


def get_course_info(courses_list, browser, driverpath):
    courses_info = []
    for url in courses_list:
        if not browser:
            html = get_response_firefox(url, driverpath)
        else:
            html = get_response_chrome(url, driverpath)
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.text.split('|')[0]
        language = soup.select_one('.ProductGlance > :last-of-type h4').text
        weaks = get_weaks(soup)
        rating = get_rating(soup)
        start_date = get_start_date(soup)
        courses_info.append([title, language, start_date, weaks, rating])
    return courses_info


def output_courses_info_to_xlsx(filepath, courses_info):
    xlsx = Workbook()
    courses_xlsx = xlsx.active
    courses_xlsx.append(['Course name', 'Language', 'Start Date', 'Number of Weeks', 'Rating'])
    for course_info in courses_info:
        courses_xlsx.append(course_info)
    xlsx.save(filepath)


if __name__ == '__main__':
    args = get_args()
    courses_list = get_courses_list(args.count)
    browser = args.browser
    driverpath = args.geckodriver
    courses_info = get_course_info(courses_list, browser, driverpath)
    filepath = path.join(args.output, 'courses.xlsx')
    output_courses_info_to_xlsx(filepath, courses_info)
