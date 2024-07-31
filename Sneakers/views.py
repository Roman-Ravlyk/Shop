import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Sneakers, Brand
from django.views import View

class SneakersListView(ListView):
    model = Sneakers

    def get_queryset(self):
        return Sneakers.objects.all()

    def get(self, request, brand_name, *args, **kwargs):
        brand = get_object_or_404(Brand, name=brand_name)
        sneakers = Sneakers.objects.filter(brand=brand)
        data = [{'id': sneaker.id, 'name': sneaker.name, 'price': sneaker.price, 'appointment': sneaker.appointment, 'material': sneaker.material} for sneaker in sneakers]
        return JsonResponse(data, safe=False)

    def render_to_response(self, context, **response_kwargs):
        sneakers = list(context['object_list'].values('id', 'name', 'price', 'appointment', 'material', 'brand_id'))
        return JsonResponse(sneakers, safe=False)

    @method_decorator(csrf_exempt)
    def post(self, request, brand_name, *args, **kwargs):
        brand = get_object_or_404(Brand, name=brand_name)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "Message": "Invalid JSON"}, status=400)

        name = data.get('name')
        price = data.get('price')
        appointment = data.get('appointment')
        material = data.get('material')


        if name and price and appointment and material:
            sneakers = Sneakers.objects.create(name=name, price=price, appointment=appointment, material=material, brand=brand)
            return JsonResponse({'status': 'Successfully added your new sneakers', 'Name': sneakers.name, 'Price': sneakers.price, 'Appointment': sneakers.appointment, 'material': sneakers.material, 'brand': brand.name})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to add your sneakers'}, status=400)

class BrandsListView(ListView):
    model = Brand

    def get_queryset(self):
        return Brand.objects.all()

    def render_to_response(self, context, **response_kwargs):
        brands = list(context['object_list'].values('id', 'name'))
        return JsonResponse(brands, safe=False)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "Message": "Invalid JSON"}, status=400)

        name = data.get('name')
        if name:
            brand = Brand.objects.create(name=name)
            return JsonResponse({'status': 'success', 'id': brand.id, 'name': brand.name})
        else:
            return JsonResponse({'status': 'error', 'message': 'Name not provided'}, status=400)
