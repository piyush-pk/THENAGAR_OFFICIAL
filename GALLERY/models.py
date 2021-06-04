from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ManyToManyField("Location")
    time = models.TimeField(auto_now_add=True)
    

    def get_location(self):
        return self.location.all()


    def __str__(self):
        return self.name 

class Log(models.Model):
    ip = models.CharField(max_length=50)
    action = models.CharField(max_length = 50)
    login = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True)

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to="thumbnail")
    url_slug = models.SlugField()
    tags = TaggableManager()
    time = models.TimeField(auto_now_add=True)


    def __str__(self):
        return self.name



class Photo(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="uploads")
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    # tags = TaggableManager()
    caption = models.CharField(max_length=250)
    time = models.TimeField(auto_now_add=True)


    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True



    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=254)
    desc = models.TextField()
    time = models.TimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Staff_user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    facebook = models.URLField(max_length=200)
    instagram = models.URLField(max_length=200)
    image = models.ImageField(upload_to="staff")
    post = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name



