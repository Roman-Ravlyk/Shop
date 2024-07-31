import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views import View
from .models import UserBuyHistory
from django.contrib.auth.models import User


class UserBuyHistoryView(ListView):
    model = UserBuyHistory

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        print(f"Fetching history for user_id: {user_id}")
        if user_id:
            queryset = UserBuyHistory.objects.filter(user_id=user_id)
            print(f"Found {queryset.count()} items in gistory for user_id: {user_id}")
            return queryset
        else:
            return UserBuyHistory.objects.none()

    def render_to_response(self, context, **response_kwargs):
        histories = context['object_list']
        history_data = []
        for history in histories:
            history_data.append({
                'username': history.user.username,
                'sneakers': history.sneakers.name
            })
        return JsonResponse(history_data, safe=False)


class AddToUserBuyHistory(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            sneakers_id = data.get('sneakers_id')

            if user_id and sneakers_id:
                new_history_object = UserBuyHistory.objects.create(user_id=user_id, sneakers_id=sneakers_id)
                new_history_object.save()
                return JsonResponse({'status': 'Successfully added to BuyHistory'}, status=200)
            else:
                return JsonResponse({'status': 'Invalid Request'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Invalid JSON'}, status=400)