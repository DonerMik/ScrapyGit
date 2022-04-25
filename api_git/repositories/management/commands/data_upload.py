import os
import csv
from bson.json_util import dumps
from pymongo import MongoClient
import json

from django.core.management.base import BaseCommand
from django.conf import settings


from repositories.models import GitLink, LastCommit, LastRelease, Repositories


class Command(BaseCommand):
    help = 'Export data MongoDB and loading data into the database'

    def handle(self, *args, **kwargs):
        print(settings.BASE_DIR)
        # DATAFILES_DIRS = os.path.join(settings.STATICFILES_DIRS[0], 'data/')
        # file_name = DATAFILES_DIRS + 'users.csv'

        client = MongoClient()
        db = client.ScrapyGit
        collection = db.repositories
        cursor = collection.find({})
        count = 0

        def get_name_item(value):
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
            print('юзерлинк создан')
            # if item['info_last_commit'] != 0:
            #     item_commit = item['info_last_commit']
            #     LastCommit.objects.create(
            #         author=item_commit.get('author'),
            #         name=item_commit.get('name'),
            #         datetime=item_commit.get('datetime_UTC')
            #     )
            #     print('ласт коммит создан')
            #
            # if item['info_last_release'] != 0:
            #     item_release = item['info_last_release']
            #     LastRelease.objects.create(
            #         version=item_release.get('version'),
            #         datetime=item_release.get('datetime_UTC'),
            #         changelog=item_release.get('changelog'),
            #         repositories=
            #     )
            #     print('Ласт релиз ок')
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
                count_release=item.get('count_release'),)
                # last_commit=LastCommit.objects.get_or_create(item.get('info_last_commit')),
                # last_release=LastRelease.objects.get(
                #      version=item.get('info_last_release').get('version'),
                #      datetime=item.get('info_last_release').get('datetime_UTC'),
                    # )
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
                    print(f"объект №{count} не имеет коммита")

            if item['info_last_release'] != 0:
                try:
                    item_release = item['info_last_release']
                    release = LastRelease.objects.create(
                        version=item_release.get('version'),
                        datetime=item_release.get('datetime_UTC'),
                        changelog=item_release.get('changelog'))
                    new_obj.last_release = release
                    new_obj.save()
                except ValueError:
                    print(f"объект №{count} не имеет релиза")


            print('ласт коммит создан')




            count += 1
            print(count)
            print('Re[pa ок')







            # with open('collection.json', 'w') as file:
            #
            #     for document in cursor:
            #         file.write(dumps(document))
            #         file.write(',')
            #





        # DATAFILES_DIRS = os.path.join(settings.STATICFILES_DIRS[0], 'data/')
        # file_name = DATAFILES_DIRS + 'users.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Users')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             role = ''
        #             for j in range(len(User.ROLE)):
        #                 if User.ROLE[j][1] == item[3]:
        #                     role = User.ROLE[j][0]
        #                     break
        #             if role == '':
        #                 CommandError(f'Ошибка данных поля role {item[3]} позиция {i} ')
        #
        #             _, created = User.objects.get_or_create(
        #                 id=item[0],
        #                 username=item[1],
        #                 email=item[2],
        #                 role=role,
        #                 bio=item[4],
        #                 first_name=item[5],
        #                 last_name=item[6]
        #             )
        #             if created:
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        # else:
        #     CommandError(f'Файл {file_name} не найден')
        #
        # file_name = DATAFILES_DIRS + 'category.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Category')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             _, created = Category.objects.get_or_create(
        #                 id=item[0],
        #                 name=item[1],
        #                 slug=item[2],
        #             )
        #             if created:
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        # else:
        #     CommandError(f'Файл {file_name} не найден')
        #
        # file_name = DATAFILES_DIRS + 'genre.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Genre')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             _, created = Genre.objects.get_or_create(
        #                 id=item[0],
        #                 name=item[1],
        #                 slug=item[2],
        #             )
        #             if created:
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        #
        # file_name = DATAFILES_DIRS + 'titles.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Title')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             category = Category.objects.get(id=item[3])
        #             _, created = Title.objects.get_or_create(
        #                 id=item[0],
        #                 name=item[1],
        #                 year=item[2],
        #                 category=category,
        #             )
        #             if created:
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        #
        # file_name = DATAFILES_DIRS + 'genre_title.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Genre_Title')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             if not Title.objects.filter(id=item[1], genre__id=item[2]):
        #                 title = Title.objects.get(id=item[1])
        #                 genre = Genre.objects.get(id=item[2])
        #                 title.genre.add(genre)
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        #
        # file_name = DATAFILES_DIRS + 'review.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Review')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             try:
        #                 _ = Review.objects.get(id=item[0])
        #             except Review.DoesNotExist:
        #                 title = Title.objects.get(id=item[1])
        #                 author = User.objects.get(id=item[3])
        #                 Review.objects.create(
        #                     id=item[0],
        #                     title=title,
        #                     text=item[2],
        #                     author=author,
        #                     score=item[4],
        #                     pub_date=item[5]
        #                 )
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')
        #
        # file_name = DATAFILES_DIRS + 'comments.csv'
        # if os.path.exists(file_name):
        #     print('Импорт Comment')
        #     count = 0
        #     with open(file_name, "r", encoding="utf8") as fin:
        #         cin = csv.reader(fin)
        #         items = [row for row in cin]
        #         for i in range(1, len(items)):
        #             item = items[i]
        #             try:
        #                 _ = Comment.objects.get(id=item[0])
        #             except Comment.DoesNotExist:
        #                 review = Review.objects.get(id=item[1])
        #                 author = User.objects.get(id=item[3])
        #                 Comment.objects.create(
        #                     id=item[0],
        #                     review=review,
        #                     text=item[2],
        #                     author=author,
        #                     pub_date=item[4]
        #                 )
        #                 count += 1
        #         print(f'Записей : {len(items)-1}\n'
        #               f'Создано : {count}')