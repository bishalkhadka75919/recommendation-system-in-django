from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shopcart', views.shop_cart_list, name='shopcart'),
    path('addtocart/<int:product_id>', views.shop_cart_add, name='addtocart'),
    path('deletefromcart/<int:id>', views.shop_cart_delete, name='deletefromcart'),
    path('detail/<int:id>', views.order_detail, name='orderdetail'),
    path('checkout', views.shop_cart_checkout, name='checkout'),
]
