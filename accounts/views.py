from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from accounts.helpers import check_duplicate_email, update_password


class Login(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("accounts:profile")

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

        context = {
            "user": request.user
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            fname = request.POST["fname"]
            lname = request.POST["lname"]

            request.user.first_name = fname
            request.user.last_name = lname
            request.user.save()
            return JsonResponse({"status": True})
        except Exception as e:
            return JsonResponse({"status": False, "msg": "Something went wrong while updating profile information. "
                                                         "Please try again."})


def change_password(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"status": False, "msg": "Please login to continue."})

        old_password = request.POST["old_pass"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        status, details = update_password(request.user, pass1, pass2, old_password, check_prev_pass=True)
        if not status:
            return JsonResponse({"status": False, "msg": details})

        return JsonResponse({"status": True})
    except Exception as e:
        return JsonResponse({"status": False, "msg": "Something went wrong while processing password change request. "
                                                     "Please try again."})


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")
