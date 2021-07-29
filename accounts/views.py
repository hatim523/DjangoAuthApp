from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from accounts.helpers import check_duplicate_email


class Login(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            pass

        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST["email"]
            pwd = request.POST["password"]

            user = auth.authenticate(username=username, password=pwd)

            if user is None:
                print("here")
                return JsonResponse({"status": False, "msg": "Invalid username or password"})

            auth.login(request, user)

            return JsonResponse({"status": True, "url": reverse("accounts:profile")})
        except Exception as e:
            print("Exception in Login(post):", str(e))
            return JsonResponse({"status": False, "msg": "Something went wrong while processing your request. "
                                                         "Please try again."})


class Register(View):
    template_name = "accounts/register.html"

    def get(self, request):
        # check if user is already logged in
        if request.user.is_authenticated:
            return redirect("accounts:profile")

        return render(request, self.template_name)

    def post(self, request):
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]

        # checking for duplicate email
        if check_duplicate_email(email):
            return JsonResponse({"status": False, "msg": "An account with entered email already exists."})

        # checking for password match
        if password != password2:
            return JsonResponse({"status": False, "msg": "Passwords do not match."})

        # creating user account
        user_obj = User.objects.create(
            first_name=fname,
            last_name=lname,
            username=email,
            email=email,
        )
        # set user password
        user_obj.set_password(password)
        user_obj.save()
        # authenticating and logging in user
        auth.login(request, user_obj)

        return JsonResponse({"status": True, "url": reverse("accounts:profile")})


class ProfilePage(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        return render(request, self.template_name)

    def post(self):
        pass


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")
