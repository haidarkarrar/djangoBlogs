from django.contrib.admin import decorators
from django.shortcuts import redirect, render
from datetime import datetime
from blogs.models import Blogs
from django.contrib.auth.models import User, auth
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        blogs = Blogs.objects.filter(author = request.user)
    else:
        blogs = None
    return render(request, 'index.html', {'blogs' : blogs})
    
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        blog = Blogs.objects.create(title = title, Description = description, date = datetime.now(), author = request.user)
        return redirect('/')
    return render(request, 'createBlog.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = {
            username : username,
            email : email,
            password : password,
            confirm_password : confirm_password
        }

        if user[password] == user[confirm_password]:
            if User.objects.filter(email = user[email]).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username = user[username]).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                new_user = User.objects.create_user(username = user[username], email = user[email], password = user[password])
                new_user.save()
                return redirect('login')
        else: 
            messages.info(request, 'Passwords does not match')    
            return redirect('register')
    else:            
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else: 
            messages.info(request, 'Username or Password is incorrect')
            return redirect('/login')
    return render(request, 'login.html') 

def logout(request):
    auth.logout(request)
    return redirect('/')