from django.db import models


class GitLink(models.Model):
    link = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.CharField(max_length=200)


class LastCommit(models.Model):
    author = models.CharField(max_length=200,
                              blank=True,
                              null=True)
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField()


class LastRelease(models.Model):
    version = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    changelog = models.TextField(blank=True,
                                 null=True)


class Repositories(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    about = models.TextField(blank=True,
                             null=True)
    site = models.CharField(max_length=200,
                            blank=True,
                            null=True
                            )
    count_stars = models.IntegerField(blank=True,
                                      null=True)
    count_forks = models.IntegerField(blank=True,
                                      null=True)
    count_watching = models.IntegerField(blank=True,
                                         null=True)
    count_commit = models.IntegerField(blank=True,
                                       null=True)

    count_release = models.IntegerField(blank=True,
                                        null=True)
    user_link = models.ForeignKey(GitLink,
                                  on_delete=models.CASCADE,
                                  related_name='repositories')
    last_commit = models.ForeignKey(LastCommit,
                                    on_delete=models.CASCADE,
                                    related_name='repositories',
                                    blank=True,
                                    null=True
                                    )
    last_release = models.ForeignKey(LastRelease,
                                     on_delete=models.CASCADE,
                                     related_name='repositories',
                                     blank=True,
                                     null=True)

    def __str__(self):
        return self.name
