from django.db import models

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
class Category(models.Model):
#    id = models.IntegerField(primary_key=True,)
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'category'
    def __unicode__(self):
        return self.name
    
class Book(models.Model):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 200)
    imageurl = models.CharField(max_length = 200)
    contenturl = models.CharField(max_length = 200)
    categorys = models.ManyToManyField(Category,through = "BookCategory")
    
    class Meta:
        db_table = 'book'
    def __unicode__(self):
        return self.name   
    
class User(models.Model):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    favoritebooks = models.ManyToManyField(Book,through = "BookMark")
    regtime = models.DateField()
    class Meta:
        db_table = 'user'
    def __unicode__(self):
        return self.name
    
class BookMark(models.Model):
#    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    attime = models.DateField()
    
    class Meta:
        db_table = 'bookmark'
    def __unicode__(self):
        return self.name
    
class BookCategory(models.Model):
#    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Book)
    category = models.ForeignKey(Category)

    class Meta:
        db_table = 'bookcategory'
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
#    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length = 200)
    attime = models.DateField()
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    class Meta:
        db_table = 'comment'
    def __unicode__(self):
        return self.book