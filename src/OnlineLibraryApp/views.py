from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
# Create your views here.
class Person(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def say(self):
        return "my name is " + self.name
    
def index(request):
    t = loader.get_template("index.html")
    user = {"name":"tom","age":23,"sex":"male"}

    person = Person("jack", 25, "female")

    book_list = ["python","ruby","java","c"]
    
    c = Context({"title":"django","user":person,"book_list":book_list})
    return HttpResponse(t.render(c))
