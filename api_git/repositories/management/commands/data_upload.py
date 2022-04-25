import csv
import json
import os

from bson.json_util import dumps
from django.conf import settings
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from repositories.models import GitLink, LastCommit, LastRelease, Repositories


class Command(BaseCommand):
    help = 'Export data MongoDB and loading data into the database'

    def handle(self, *args, **kwargs):
        '''Функция загружает данные с MongoDB в базу данных Django'''
        print(settings.BASE_DIR)

        client = MongoClient()
        db = client.ScrapyGit
        collection = db.repositories
        cursor = collection.find({})
        count = 0

        def get_name_item(value):
            '''Функция обрезает домен, оставляя название репозитория'''

            value = value[19:]
            if value[-1] == '/':
                return value[:-1]
            return value

        for item in cursor:
            name_item = get_name_item(item['user_url'])
            GitLink.objects.get_or_create(
                link=item['user_url'],
                slug=name_item
            )
            print('GitLink создан')

            new_obj = Repositories.objects.create(
                name=item.get('name'),
                url=item.get('url'),
                user_link=GitLink.objects.get(
                    link=item.get('user_url')),
                about=item.get('about'),
                site=item.get('site'),
                count_stars=item.get('count_stars'),
                count_forks=item.get('count_forks'),
                count_watching=item.get('count_watching'),
                count_commit=item.get('count_commit'),
                count_release=item.get('count_release')
            )

            if item['info_last_commit'] != 0:
                try:
                    item_commit = item['info_last_commit']
                    if not item_commit.get('author'):
                        item_commit['author'] = 'Ошибка чтения автора'

                    new_commit = LastCommit.objects.create(
                        author=item_commit.get('author'),
                        name=item_commit.get('name'),
                        datetime=item_commit.get('datetime_UTC')
                    )
                    new_obj.last_commit = new_commit
                    new_obj.save()

                except ValueError:
                    print(f"Oбъект №{count} не имеет коммита")

            if item['info_last_release'] != 0:
                try:
                    item_release = item['info_last_release']
                    release = LastRelease.objects.create(
                        version=item_release.get('version'),
                        datetime=item_release.get('datetime_UTC'),)
                    release.changelog = item_release.get('changelog')
                    release.save()
                    new_obj.last_release = release
                    new_obj.save()
                except ValueError:
                    print(f"объект №{count} не имеет релиза")

            count += 1
            print(f'Объект № {count} загружен')

        print(f'Колличество загруженных элементов {count})')
        print('База данных загружена')
