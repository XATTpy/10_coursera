import requests
from lxml import html, etree
from random import shuffle


def get_courses_list():
    courses_list = []
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    request = requests.get(url).content
    tree = html.fromstring(request)

    for loc in tree.xpath('.//url/loc'):
        url = loc.text
        courses_list.append(url)
    shuffle(courses_list)
    return courses_list[:20]


def get_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    courses_list = get_courses_list()
    print(len(courses_list))
