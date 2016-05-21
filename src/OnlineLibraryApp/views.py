import logging
import random
from django.core.mail import send_mail  
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
from django.template.context_processors import request

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

SENTCODE = False
flag = False
PREURL = None
VERIFYCODE = None

def init():
    global SENTCODE,PREURL
    SENTCODE = False
    PREURL = None
    
def global_setting(request):
    #init()#init befor reg error
    return{'SITE_URL': settings.SITE_URL,
           'SITE_NAME': settings.SITE_NAME,
           'SITE_DESC': settings.SITE_DESC,
           'WEIBO_SINA': settings.WEIBO_SINA,
           'WEIBO_TENCENT': settings.WEIBO_TENCENT,
           'PRO_RSS': settings.PRO_RSS,
           'PRO_EMAIL': settings.PRO_EMAIL,
           }

def index(request):
    init()
    try:
        index_bookList = Book.objects.all()[:12]
        
    except Exception as e:
        logger.error(e)

        
    return render(request, 'index.html', locals())

def booklist(request):
    init()
    try:
        cid = request.GET.get('category',None)
        kid = request.GET.get('keyword',None)
        fid = request.GET.get('favorites',None)
        if (fid):
            fid = request.user.id
            print fid
            user = User.objects.all().get(id = fid)
            print user
            #bookList = user.favoritebooks.all()
            bookList = getPage(request, user.favoritebooks.all())
            #print ("123")
#             for b in bookList:
#                 print b
        else:
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
                #for b in bookList:
                #    print b
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
    init()
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
    init()
    try:   
        id = request.GET.get('id', None)
        
        try:
            book = Book.objects.all().get(id=id)
            
            if request.user.is_authenticated():
                print
                likeRecord = BookMark.objects.all().filter(book_id__exact = id, user__exact = request.user)
#                 for r in likeRecord:
#                     print r
                if likeRecord:
                    isLike = True
                else:
                    isLike = False
            else:
                pass
            
            
            commentList = book.comment_set.all()
            '''
            print book
            if book:
                pass
            else:
                print ("1213")
                return render(request, 'failure.html', {'reason': ''})
            '''
        except Book.DoesNotExist:
            
            return render(request, 'failure.html', {'reason': ''})
        
        

            
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
            if request.user.is_authenticated():
                comment = Comment(username=comment_form.cleaned_data["author"],
                                  email=comment_form.cleaned_data["email"],
                                  content=comment_form.cleaned_data["comment"],
                                  book_id=comment_form.cleaned_data["book"],
                                  user=request.user)
            else:
                defaultUser=User.objects.all().get(id=6)
                comment = Comment(username=comment_form.cleaned_data["author"],
                                  email=comment_form.cleaned_data["email"],
                                  content=comment_form.cleaned_data["comment"],
                                  book_id=comment_form.cleaned_data["book"],
                                  user=defaultUser)
            #print(request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_like(request):
    #print ("tests")
    try:
        #print ("tests")
        if request.user.is_authenticated():
            '''
            bid = request.GET.get('id',None)
            user = User.objects.get(id = request.user.id)
            book = Book.objects.get(id = bid)
            user.favoritebooks.add(book)
            '''
            bookmark = BookMark(user = request.user,
                                book_id = request.GET.get('id',None))
            bookmark.save()
            
        else:
            pass
    except Exception as e:
        print e
        logger.error(e)
        
    return redirect(request.META['HTTP_REFERER'])

def do_unlike(request):
    #print ("tests")
    try:
        #print ("tests")
        if request.user.is_authenticated():
            BookMark.objects.all().filter(book_id__exact = request.GET.get('id',None), user__exact = request.user).delete()

            
        else:
            pass
    except Exception as e:
        print e
        logger.error(e)
        
    return redirect(request.META['HTTP_REFERER'])

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

def createVerifyCode(): 
    chars=['0','1','2','3','4','5','6','7','8','9'] 
    x = random.choice(chars),random.choice(chars),random.choice(chars),random.choice(chars) 
    verifyCode = "".join(x) 
    return verifyCode 

def do_reg(request):
    
    #print "123"
    #send_mail('Register Verification - Online Library', createVerifyCode() , 'w424065448@126.com', ['424065448@qq.com'], fail_silently=False)
    global SENTCODE,PREURL,VERIFYCODE
    localSentCode = SENTCODE

    
    try:
        
        if request.method == 'POST':

                #print "123"
                #send_mail('Register Verification - Online Library', createVerifyCode() , 'w424065448@126.com', [regEmail], fail_silently=False)
                reg_form = RegForm(request.POST)
                
                #print SENTCODE
                #return render(request, 'reg.html', locals())
#                 print reg_form
                
#                 print email
                print SENTCODE
                print VERIFYCODE
                if SENTCODE:
                    print "test1"
                    if reg_form.is_valid():
                        vcode = reg_form.cleaned_data["verifycode"]
                        
                        if vcode == VERIFYCODE:
                            print "test2"
                            user = User(username=reg_form.cleaned_data["username"],
                                        email=reg_form.cleaned_data["email"],
                                        password=make_password(reg_form.cleaned_data["password"]),
                                        )
                            #user = User.objects.create(username=reg_form.cleaned_data["username"],
                            #            email=reg_form.cleaned_data["email"],
                            #            password=make_password(reg_form.cleaned_data["password"]),)
                            print(user)
                            user.save()
            
                            
                            user.backend = 'django.contrib.auth.backends.ModelBackend' 
                            login(request, user)
                           
                            return redirect(PREURL)
                        else:
                            return render(request, 'failure.html', {'reason': 'verify code errror'})
                    else:
                        
                        return render(request, 'failure.html', {'reason': reg_form.errors})
                else:
                    print "test3"
                    reg_form.is_valid()#clean in this method
                    regEmail = reg_form.cleaned_data["email"]

                    #regEmail=reg_form.cleaned_data["email"]
                    VERIFYCODE = createVerifyCode()
                    send_mail('Register Verification - Online Library', VERIFYCODE, 'w424065448@126.com', [regEmail], fail_silently=False)
                    print "sent email"
                    PREURL = request.POST.get('source_url')
                
                
                SENTCODE = True
                localSentCode = SENTCODE
                print SENTCODE
                
        else:

            #reg_form = RegForm({'username':'default_name','password':make_password('123465'),'verifycode':'default_code','email':''})
            reg_form = RegForm()
            #verify_form = VerifyForm()#noticc this!
    except Exception as e:
        logger.error(e)

    return render(request, 'reg.html', locals())


'''

def do_reg(request):
    #print "123"
    #send_mail('Register Verification - Online Library', createVerifyCode() , 'w424065448@126.com', ['424065448@qq.com'], fail_silently=False)
    global flag
    global preurl
    
    try:
        
        if request.method == 'POST':
            SENTCODE = True
            if SENTCODE:
                #print "123"
                #send_mail('Register Verification - Online Library', createVerifyCode() , 'w424065448@126.com', [regEmail], fail_silently=False)
                reg_form = RegForm(request.POST)
                print "test0" 
                regEmail = reg_form.cleaned_data["email"]
                print reg_form
                send_mail('Register Verification - Online Library', createVerifyCode() , 'w424065448@126.com', [regEmail], fail_silently=False)
                #print SENTCODE
                #return render(request, 'reg.html', locals())
#                 print reg_form
                
#                 print email
                print flag
                if flag:
                    print "test1"
                    if reg_form.is_valid():
                        print "test2"
                        user = User(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),
                                    )
                        #user = User.objects.create(username=reg_form.cleaned_data["username"],
                        #            email=reg_form.cleaned_data["email"],
                        #            password=make_password(reg_form.cleaned_data["password"]),)
                        print(user)
                        user.save()
        
                        
                        user.backend = 'django.contrib.auth.backends.ModelBackend' 
                        login(request, user)
                       
                        return redirect(preurl)
                    else:
                        SENTCODE = False
                        return render(request, 'failure.html', {'reason': reg_form.errors})
                else:
                    
                    preurl = request.POST.get('source_url')
                    
                flag = True
            else:

                
        else:

            #reg_form = RegForm({'username':'default_name','password':make_password('123465'),'verifycode':'default_code','email':''})
            reg_form = RegForm()
            #verify_form = VerifyForm()#noticc this!
    except Exception as e:
        logger.error(e)

    return render(request, 'reg.html', locals())


def do_reg(request):
    try:
        if request.method == 'POST':
            sentVcode = True
            reg_form = RegForm(request.POST)
            email = reg_form.cleaned_data["email"]
            print email
            if reg_form.is_valid():

                user.save()

                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm({'username':'default_name','password':make_password('123465'),'verifycode':'default_code','email':''})

    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

'''


# def do_verify(request):
#     try:
#         if request.method == 'POST':
#              
#             verify_form = VerifyForm(request.POST)
#             print verify_form
#             if verify_form.is_valid():
#                 print verify_form.email
# #                 return render(request, 'reg.html', locals())
#             else:
#                 return render(request, 'failure.html', {'reason': verify_form.errors})
#         else:
#             verify_form = VerifyForm()
#     except Exception as e:
#         logger.error(e)
#     return render(request, 'reg.html', locals())

def do_login(request):
    init()
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


