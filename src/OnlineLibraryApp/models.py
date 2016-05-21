from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
'''
class Student(models.Model):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 50)
    age = models.IntegerField()

    class Meta:
        db_table = 'student'
    def __unicode__(self):
        return self.name
'''   
from test.test_imageop import MAX_LEN
from django.template.defaultfilters import default

class Category(models.Model):
#    id = models.IntegerField(primary_key=True,)
    name = models.CharField(max_length = 50, default="category")
    imageurl = models.CharField(max_length = 200, default="")
    class Meta:
        db_table = 'category'
    def __unicode__(self):
        return self.name
    
class Book(models.Model):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 100, default="book")
    author = models.CharField(max_length = 100, default="author", blank=True)
    description = models.CharField(max_length = 200, default="Enjoy Reading!")
    imageurl = models.CharField(max_length = 200, default="http://www.readanybook.com/covers/105799/small")
    contenturl = models.CharField(max_length = 200, default="#")
    categorys = models.ManyToManyField(Category,through = "BookCategory")
    largeimageurl = models.CharField(max_length = 200, default="http://www.readanybook.com/covers/105799/big")
    class Meta:
        db_table = 'book'
        ordering = ['-id']
    def __unicode__(self):
        return self.name   
    
class User(AbstractUser):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 50, default="new user")
    simple_password = models.CharField(max_length = 50, default="123456")
    favoritebooks = models.ManyToManyField(Book,through = "BookMark")
    regtime = models.DateField(auto_now_add = True)
    phone_number = models.CharField(max_length = 50, default="13900000000")
    class Meta:
        db_table = 'user'
    def __unicode__(self):
        return self.username
    
class BookMark(models.Model):
#    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    attime = models.DateField(auto_now_add = True)
    
    class Meta:
        db_table = 'bookmark'
    def __unicode__(self):
        return self.user.name+':'+self.book.name
    
class BookCategory(models.Model):
#    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Book)
    category = models.ForeignKey(Category)

    class Meta:
        db_table = 'bookcategory'
    def __unicode__(self):
        return self.category.name+':'+self.book.name
    
class Comment(models.Model):
#    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length = 200, default="new comment")
    attime = models.DateTimeField(auto_now_add = True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User, blank=True)
    rank = models.IntegerField(default=5)
    class Meta:
        db_table = 'comment'
    def __unicode__(self):
        return self.user.name + ":" + self.book.name