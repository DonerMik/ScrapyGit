from repositories.models import GitLink, LastCommit, LastRelease, Repositories
from rest_framework import serializers


class GitlinkSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('link',)
        model = GitLink


class LastCommitSerializer(serializers.ModelSerializer):

    class Meta:
        fields =('__all__')
        model = LastCommit


class LastReleaseSerializer(serializers.ModelSerializer):

    class Meta:
        fields =('__all__')
        model = LastRelease


class RepositoriesSerializer(serializers.ModelSerializer):
    user_link = GitlinkSerializer()
    last_commit = LastCommitSerializer()
    last_release = LastReleaseSerializer()

    class Meta:
        fields = ('name', 'about', 'site', 'count_stars',
                  'count_forks', 'count_watching', 'count_commit', 'count_release',
                  'user_link', 'last_commit', 'last_release',)
        model = Repositories
