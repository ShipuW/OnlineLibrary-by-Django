
from django import forms
from django.conf import settings
from django.db.models import Q
from models import User
import re

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username cannot null",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password cannot null",})

class RegForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username cannot null",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email cannot null",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password cannot null",})


class CommentForm(forms.Form):

    author = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "name", "id": "name", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),
                              max_length=50,error_messages={"required":"username cannot be null",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "email","id":"email","type":"email","class": "comment_input",
                                                           "required":"required","size":"25", "tabindex":"2"}),
                                 max_length=50, error_messages={"required":"email cannot be null",})
    comment = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "write your comment!","id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                                                    error_messages={"required":"comment cannot be null",})
    book = forms.CharField(widget=forms.HiddenInput())


