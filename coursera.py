from lxml import html, etree
from random import shuffle
from bs4 import BeautifulSoup
import requests
import re
from openpyxl import Workbook
from os import path
import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description='Данные о курсах на Курсере.')
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


def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'itemprop': 'ratingValue'}).text
    except AttributeError:
        rating = 'Unknown'
    return rating


def get_weeks(soup):
    try:
        weeks = len(soup.find(class_='Syllabus').find_all('div', text = re.compile('Week')))
    except AttributeError:
        weeks = 'Unknown'
    return weeks


def get_course_info(courses_list):
    courses_info = []
    for url in courses_list:
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.text.split('|')[0]
        language = soup.select_one('.ProductGlance > :last-of-type h4').text
        start_date = soup.find(id="start-date-string").text.replace('Starts ', '')
        weeks, rating = get_weeks(soup), get_rating(soup)
        courses_info.append([title, language, start_date, weeks, rating])
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
    time4load = args.time
    courses_info = get_course_info(courses_list)
    filepath = path.join(args.output, 'courses.xlsx')
    output_courses_info_to_xlsx(filepath, courses_info)
