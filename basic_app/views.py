from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):

    # Assume at first they are not registered
    registered = False

    # If request == 'post'
    if request.method == 'POST':

        # We grab information from the forms
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        # We check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            
            """IF VALID WE GRAB EVERYTHING FROM USER FORM"""
            # 1. Saving from into DB
            user = user_form.save()
            # 2. Hashing password
            user.set_password(user.password)
            # 3. Save hashed password to DB
            user.save()

            """THEN WE GRAB THE PROFILE FORM AND CHECK IF THERE'S A PICTURE BEFORE SAVING"""
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True

        else:

            # If method was POST, but we had an error we'll print them out
            print(user_form.errors, profile_form.errors)
    
    else:

        # Request method NOT Post \ we just set the forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password: {}".format(username, password))
            return HttpResponse("INVALID LOGIN DETAILS")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def special(request):
    return HttpResponse('You are Logged in')