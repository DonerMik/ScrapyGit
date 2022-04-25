from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import GitLinkViewSet, RepositoriesViewSet, count_links, count_repositories, avg_repositories, \
    max_commit_repository, avg_stars_repository

router = DefaultRouter()

router.register(r'list_link/(?P<slug>\w+)', RepositoriesViewSet, basename='repositories')
router.register('list_link', GitLinkViewSet, basename='gitlinks')

urlpatterns = [
    path('', include(router.urls)),
    path('count_links', count_links),
    path('count_repositories', count_repositories),
    path('avg_repositories', avg_repositories),
    path('max_commit_repository', max_commit_repository),
    path('avg_stars_repository', avg_stars_repository)
]


