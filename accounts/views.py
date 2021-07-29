from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View


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

            return JsonResponse({"status": True, "url": ""})
        except Exception as e:
            print("Exception in Login(post):", str(e))
            return JsonResponse({"status": False, "msg": "Something went wrong while processing your request. "
                                                         "Please try again."})
