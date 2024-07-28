import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from .models import UserShoppingCart
from django.contrib.auth.models import User
from Sneakers.models import Sneakers

class CartListView(ListView):
    model = UserShoppingCart

    def get_queryset(self):
        return UserShoppingCart.objects.all()

    def render_to_response(self, context, **response_kwargs):
        carts = list(context['object_list'].values('name'))
        return JsonResponse(carts, safe=False)

class AddToCart(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get('user')
            sneakers_id = data.get('sneakers')

            if user_id and sneakers_id is not None:
                user = get_object_or_404(User, id=user_id)
                sneakers = get_object_or_404(Sneakers, id=sneakers_id)
                cart_object, created = UserShoppingCart.objects.get_or_create(user=user, sneakers=sneakers)
                if created:
                    return JsonResponse({"status": "Successfully added to cart", "sneakers": sneakers.name}, status=200)
                else:
                    return JsonResponse({"status": "info", "message": "Item already in cart"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Failed to add to cart"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

class ChangeCartObj(View):
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get('user')
            sneakers_id = data.get('sneakers')

            if user_id and sneakers_id is not None:
                user = get_object_or_404(User, id=user_id)
                sneakers = get_object_or_404(Sneakers, id=sneakers_id)

                deleted, _ = UserShoppingCart.objects.filter(user=user, sneakers=sneakers).delete()
                if deleted:
                    return JsonResponse({"status": "Successfully removed from cart", "sneakers": sneakers.name}, status=200)
                else:
                    return JsonResponse({"status": "info", "message": "Item not found in cart"}, status=400)
            else:
                return JsonResponse({"status": "error", "message": "Failed to remove from cart"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
