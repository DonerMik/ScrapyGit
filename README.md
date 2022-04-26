ScrapyGit — В данном проекте реализовано два сервиса:

1)проект для сбора информации о репозиториях с сайта github.com и передачи их в базу данных.

2)API для предоставления информации о репозиториях и общей статистики имеющихся данных.

В данном проекте исользовались следующие технологии:
- Python 3.8(весь проект написан на данном ЯП)
- scrapy(парсер)  
- MongoDB(данные парсера сохраняются в данную БД)
- Django 4.0.4(фреймворк для разработки вебприложения)
- Django restframework 3.13.1(API фреймворк для Django)
- sqlite3

ОСНОВНЫЕ НАСТРОЙКИ ПРОЕКТА:

1)Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/account_name/api_yamdb/

2)Перейти в проект.

3)Cоздать и активировать виртуальное окружение:

python3 -m venv env

source env/bin/activate

4)Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip

pip install -r requirements.txt

5)Установить и запустить сервер MongoDB 


НАСТРОЙКА API:

1)Перейдите в папку проекта api_git

2)Выполнить миграции:

python3 manage.py migrate

3)Запустить проект(при необходимости):

python3 manage.py runserver


РАБОТА СЕРВИСА SCRAPY_GIT


SCRAPY_GIT:

- перейдите в папку scrapy_git

- запустите спайдер командой в терминале:

  scrapy crawl git-spider

- в терминале появится предложение: "Введите ссылки".
Программа принимает одну и более ссылок записанных через пробел.

- нажмите "ENTER".
Процесс парсинга информации и сохрание её в базу данных MongoDB начался.
В базе данных будет создана коллекия "repositories".
Примечание: если данная коллекция имеется, то данные будут добавлены 
в указанную коллекцию.


РАБОТА СЕРВИСА API_GIT:

Для загрузки данных из MongoDB в sqlite3 перейти в папку проекта api_git/
Запуск загрузчика данных вызывается командой в терминале:
  
  python manage.py data_upload

После выполнения команды указанной выше, данные загружены в БД sqlite3

Для запуска сервиса необходимо запустить его веб-приложение:

  python manage.py runserver

Проект запущен локально и доступен по пути указанном в терминале.


API_GIT предоставляет информацию по следующим эндпойтам:

1)Информация о имеющихся пользователья и проектах в сервисе:
127.0.0.1:8000/api/list_link/

2)Информация о репозиториях пользователя:
127.0.0.1:8000/api/list_link/<имя проекта или пользователя>

3)Информация о колличестве имеющихся пользователей:
127.0.0.1:8000/api/list_link/count_links

4)Информация о среднем колличестве репозиториев имеющихся у пользователей
127.0.0.1:8000/api/avg_repositories

5)Информация о репозитории с максимальным колличеством коммитов:
127.0.0.1:8000/api/max_commit_repository

6)Информация о среднем колличестве звезд имеющихся репозиториев:
127.0.0.1:8000/api/avg_stars_repository
