import logging
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, Context, RequestContext
from models import Category, Book, User, BookMark, BookCategory, Comment
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.conf import settings

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
        bookList = Book.objects.all()
        paginator = Paginator(bookList, 12)
        try:
            page = int(request.GET.get('page',1))
            bookList = paginator.page(page)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            bookList = paginator.page(1)
                
    except Exception as e:
        logger.error(e)
        
    return render(request, 'booklist.html', locals())

def category(request):
    try:
        categoryList = Category.objects.all()
    except Exception as e:
        logger.error(e)
        
    return render(request, 'category.html', locals())
        
'''        
def column(request):
    try:
        cid = request.GET.get('cid', None)
        try:
            pass
            category = Category.objects.get(pk=cid)
        except (cid != '1', cid != '2'):
            return render(request, 'failure.html', {'reason': ''})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())
    '''