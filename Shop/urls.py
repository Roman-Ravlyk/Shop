from django.contrib import admin
from django.urls import path

from Sneakers.views import SneakersListView, BrandsListView
from authentication.views import RegisterView, LoginView, LogoutView, PasswordChangeView, UpdateUserNameView
from shopping_cart.views import CartListView, ChangeCartObj, AddToCart
from user_history .views import AddToUserBuyHistory, UserBuyHistoryView

urlpatterns = [

    path('admin/', admin.site.urls),

    #Sneakers
    path('brands/', BrandsListView.as_view(), name='brands list'),
    path('sneakers/brand/<str:brand_name>', SneakersListView.as_view(), name='brand_sneakers'),

    #Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='register'),
    path('changepassword/', PasswordChangeView.as_view(), name='change password'),
    path('changeusername/', UpdateUserNameView.as_view(), name='change username'),

    #User cart
    path('getcart/<int:user_id>', CartListView.as_view(), name='cart querylist'),
    path('changecart/', ChangeCartObj.as_view(), name='delete object from cart'),
    path('addtocart/', AddToCart.as_view(), name='add obj to cart'),

    #User buy history
    path('addtohistory/', AddToUserBuyHistory.as_view(), name='add obj to history'),
    path('gethistory/<int:user_id>', UserBuyHistoryView.as_view(), name='history querylist'),

]
