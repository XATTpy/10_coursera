# Данные о курсах на Курсере

Этот скрипт находит информацию о случайных курсах на [COURSERA.org](https://www.coursera.org) и записывает её в xlsx-файл.

# Как использовать

Для работы скрипта нужен установленный браузер Firefox/Chrome. 

При этом, необходим ещё ```geckodriver```/```chromedriver```. Скачать его можно по ссылке:
* Для фаерфокса: https://github.com/mozilla/geckodriver/releases/
* Для хрома: https://sites.google.com/a/chromium.org/chromedriver/downloads

После запуска скрипта будут открываться окна браузера - это нормально. Их можно закрывать, но осторожно: нельзя закрывать окно браузера на котором идёт сбор информации. 
Это необходимо, чтобы загрузить все скрипты страницы, которые могут содержать нужную информацию.

При запуске скрипта с флагом -h можно получить информацию об аргументах:
```bash
$ python3 coursera.py -h
usage: coursera.py [-h] [-b BROWSER] [-o OUTPUT] [-c COUNT] geckodriver

Данные о курсах на Курсере.

positional arguments:
  geckodriver           Введите путь к скаченному geckodriver.

optional arguments:
  -h, --help            show this help message and exit
  -b BROWSER, --browser BROWSER
                        Если используете Chrome, то введите 1 (если Firefox,
                        то ничего не вводите)
  -o OUTPUT, --output OUTPUT
                        Введите путь для сохранения xlsx-файла.
  -c COUNT, --count COUNT
                        Введите количество курсов.
```

# Быстрый запуск
Используй pip(или pip3) для установки всех зависимостей:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Помните, рекомендуется использовать [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для лучшей изоляции.

Теперь можно запускать скрипт:

```bash
$ python3 coursera.py /path/to/geckodriver -c 5 -o /path/to/output/dir
```

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке ― [DEVMAN.org](https://devman.org)