from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'main_app/index.html')


def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                  email=request.POST['email'], password=pw_hash, birthday=request.POST['birthday'])
        request.session['uid'] = user.id
        return redirect('/success')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/success')
        else:
          messages.error(request, "Wrong password")
    return redirect('/')


def success(request):
    if 'uid' not in request.session:
        messages.error(request, "You have not logged in or registered, please log in or register.")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uid'])
    }
    return render(request, 'main_app/success.html', context)

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out.")
    return redirect('/')
