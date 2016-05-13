import logging
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, Context, RequestContext
#from models import Category, Book, User, BookMark, BookCategory, Comment
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.conf import settings
from models import *
from forms import *

from django.core.urlresolvers import reverse

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password

from django.db import connection
from django.db.models import Count

import json

logger = logging.getLogger('OnlineLibraryApp.views')

# Create your views here.
'''
class Person(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def say(self):
        return "my name is " + self.name
    
def index(request):
    t = loader.get_template("index.html")
#    user = {"name":"tom","age":23,"sex":"male"}

#    person = Person("jack", 25, "female")

#    book_list = ["python","ruby","java","c"]
    
#    c = Context({"title":"django","user":person,"book_list":book_list})
    c = Context()
    return HttpResponse(t.render(c))
'''
def global_setting(request):
    
    return{'SITE_URL': settings.SITE_URL,
           'SITE_NAME': settings.SITE_NAME,
           'SITE_DESC': settings.SITE_DESC,
           'WEIBO_SINA': settings.WEIBO_SINA,
           'WEIBO_TENCENT': settings.WEIBO_TENCENT,
           'PRO_RSS': settings.PRO_RSS,
           'PRO_EMAIL': settings.PRO_EMAIL,}

def index(request):

    try:
        index_bookList = Book.objects.all()[:12]
        
    except Exception as e:
        logger.error(e)

        
    return render(request, 'index.html', locals())

def booklist(request):
    try:
        cid = request.GET.get('category',None)
        kid = request.GET.get('keyword',None)
        if (kid):
            '''
            category_list = Category.objects.all().filter( name__icontains = kid )
            bookList2 = []
            for category in category_list:
                bookList1 =  Book.objects.all().filter( categorys__exact = category )
                bookList2.extend(bookList1)
            '''
            bookList = Book.objects.all().filter( name__icontains = kid )
            #bookList = getPage(request, set(bookList2.extend(bookList3)))
            for b in bookList:
                print b
        else:
            if (cid):
                category = Category.objects.all().get(id = cid)
                bookList = getPage(request, Book.objects.all().filter( categorys__exact = category ))
            else:
                bookList = getPage(request, Book.objects.all())

                
    except Exception as e:
        logger.error(e)
        
    return render(request, 'booklist.html', locals())

def category(request):
    try:
        categoryList = Category.objects.all()
    except Exception as e:
        logger.error(e)
        
    return render(request, 'category.html', locals())
        


def getPage(request, bookList):
    paginator = Paginator(bookList, 12)
    try:
        page = int(request.GET.get('page',1))
        bookList = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        bookList = paginator.page(1)
    return bookList

def detail(request):
    try:   
        id = request.GET.get('id', None)
        try:
            book = Book.objects.all().get(id=id)
        except Book.DoesNotExist:
            return render(request, 'failure.html', {'reason': ''})

        commentList = book.comment_set.all()
    except Exception as e:
        logger.error(e)
    
    comment_form = CommentForm({'author': request.user.username,
                                'email': request.user.email,
                                'book': id} if request.user.is_authenticated() else{'book': id})
#     print("----------------")
#     print(comment_form)
#     print("----------------")
    return render(request, 'detail.html', locals())

def comment_post(request):
    try:
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

#             print(comment_form.cleaned_data["book"])
#             print(request.user)
            comment = Comment(username=comment_form.cleaned_data["author"],
                              email=comment_form.cleaned_data["email"],
                              content=comment_form.cleaned_data["comment"],
                              book_id=comment_form.cleaned_data["book"],
                              user=request.user if request.user.is_authenticated() else None)
#             print(comment)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            
            if reg_form.is_valid():
                user = User(username=reg_form.cleaned_data["username"],
                            email=reg_form.cleaned_data["email"],
                            password=make_password(reg_form.cleaned_data["password"]),)
                #user = User.objects.create(username=reg_form.cleaned_data["username"],
                #            email=reg_form.cleaned_data["email"],
                #            password=make_password(reg_form.cleaned_data["password"]),)
                #print(user)
                user.save()

                
                user.backend = 'django.contrib.auth.backends.ModelBackend' 
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' 
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': 'login failed'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())
