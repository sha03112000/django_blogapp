from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('signIn')
    else:
        form = UserCreationForm()
    return render(request, 'authApp/signUp.html', {'form': form})



def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['id'] = user.id
            request.session['username'] = user.username
            
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authApp/signIn.html')


    
def signOut(request):
    request.session.flush()
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('signIn')
