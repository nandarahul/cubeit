from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


class Content(models.Model):
    link = models.URLField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.link

    def asDict(self):
        content_dict = {}
        content_dict["id"] = self.id
        content_dict["link"] = self.link
        return content_dict

class Cube(models.Model):
    name = models.CharField(max_length=30)
    contents = models.ManyToManyField(Content)
    users = models.ManyToManyField(User)

    def __str__(self):
        return  self.name

    def asDict(self):
        cube_dict = {}
        cube_dict["id"] = self.id
        cube_dict["name"] = self.name
        return cube_dict





