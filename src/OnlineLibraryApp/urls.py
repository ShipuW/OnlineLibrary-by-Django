
from django.conf.urls import url

from OnlineLibraryApp.views import *

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^booklist/$',booklist, name='booklist'),
    url(r'^category/$',category, name='category'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout/', do_logout, name='logout'),
    url(r'^like/', do_like, name='like'),
    url(r'^unlike/', do_unlike, name='unlike'),
    url(r'^reg/', do_reg, name='reg'),
    #url(r'^reg/', do_verify, name='verify'),
    url(r'^login/', do_login, name='login'),

]