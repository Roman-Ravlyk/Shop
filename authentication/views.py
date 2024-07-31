import json
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.http import JsonResponse


class RegisterView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'User with this username is already created'},
                                    status=400)
            else:
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                return JsonResponse({'status': 'Successfully registered', 'username': user.username}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "Message": "Invalid JSON"}, status=400)

class LoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"status": "Successfully logged in", "username": user.username}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "User is not found"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)


class LogoutView(View):
    def get(self, request):
        user = logout(request)
        return JsonResponse({"status": "Successfully logged out"}, status=200)

class PasswordChangeView(View):
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User isn`t authenticated"}, status=400)

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not user.check_password(current_password):
            return JsonResponse({"status": "error", "message": "Incorrect password"}, status=400)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({"status": "Successfully changed password"}, status=200)


class UpdateUserNameView(View):
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User isn`t authenticated"}, status=400)

        username = data.get("username")

        if username:
            user.username = username

        user.save()

        return JsonResponse({"status": "Successfully changed your profile"}, status=200)


class UpdateUserAvatar(View):
    pass