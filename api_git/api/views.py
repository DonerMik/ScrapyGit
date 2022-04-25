from django.db.models import Avg
from django.shortcuts import get_list_or_404
from repositories.models import GitLink, Repositories
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import GitlinkSerializer, RepositoriesSerializer


class GitLinkViewSet(viewsets.ModelViewSet):
    queryset = GitLink.objects.all()
    serializer_class = GitlinkSerializer
    pagination_class = LimitOffsetPagination


class RepositoriesViewSet(viewsets.ModelViewSet):
    serializer_class = RepositoriesSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        response = get_list_or_404(Repositories, user_link__slug=slug)
        return response


@api_view(['GET'])
def count_links(response):
    count_links = GitLink.objects.count()
    response = {
        "Колличество ссылок": count_links
    }
    return Response(response)


@api_view(['GET'])
def count_repositories(response):
    count_repo = Repositories.objects.count()
    response = {
        "Общее колличество репозиториев": count_repo
    }
    return Response(response)


@api_view(['GET'])
def avg_repositories(response):
    '''Предоставляет среднее колличество репозиториев у пользователя.'''

    count_links = GitLink.objects.count()
    count_repo = Repositories.objects.count()
    avg = round(count_repo/count_links, 0)
    response = {
        "avg_repositories_users": avg
    }
    return Response(response)


@api_view(['GET'])
def max_commit_repository(response):
    '''Предоставляет репозиторий с максимальным колличеством коммитов '''

    max_commit = Repositories.objects.all().order_by("-count_commit")[0]
    response = {
        "Название репозитория": max_commit.name,
        "Колличество коммитов": max_commit.count_commit
    }
    return Response(response)


@api_view(['GET'])
def avg_stars_repository(response):
    '''Предоставляет среднее колличество звезд в репозитории'''

    avg = Repositories.objects.all().aggregate(avg=Avg('count_stars'))
    response = {
        "Среднее колличество звезд": round(avg['avg'], 0)
    }
    return Response(response)
