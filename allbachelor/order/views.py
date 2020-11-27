from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import ShopCart, ShopCartForm, OrderForm, Order, OrderDetail


# Create your views here.
@login_required(login_url='/shop/login')
def index(request):
    current_user = request.user
    orders = Order.objects.all().filter(user_id=current_user.id)

    context = {'page': 'orders',
               'orders': orders,
               }
    return render(request, 'order_list.html', context)


@login_required(login_url='/shop/login')
def shop_cart_list(request):
    current_user = request.user
    shopcart = ShopCart.objects.all().filter(user_id=current_user.id)
    carttotal = 0
    for rs in shopcart:
        carttotal += rs.quantity * rs.product.discount_price
    carttax = (14/100)*carttotal
    cartwithtax= carttotal+carttax

    context = {'page': 'cart',
               'shopcart': shopcart,
               'carttotal': carttotal,
               'carttax':carttax,
               'cartwithtax':cartwithtax
               }
    return render(request, 'shop_cart_list.html', context)


@login_required(login_url='/shop/login')
def shop_cart_add(request, product_id):
    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')  #
    # return HttpResponse(url)
    form = ShopCartForm(request.POST or None)
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            current_user = request.user  # Get User id
            quantity = form.cleaned_data['quantity']  # get product quantity from form

            # Checking product in ShopCart
            try:
                q1 = ShopCart.objects.get(user_id=current_user.id, product_id=product_id)
            except ShopCart.DoesNotExist:
                q1 = None
            if q1 != None:  # Update  quantity to exist product quantity
                q1.quantity = q1.quantity + quantity
                q1.save()
            else:  # Add new item to shop cart
                data = ShopCart(user_id=current_user.id, product_id=product_id, quantity=quantity)
                data.save()
            request.session['cart_items'] = ShopCart.objects.filter(
                user_id=current_user.id).count()  # Count item in shop cart
            messages.success(request, "Product added to cart.. ")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(reverse('shop:product_detail', args=[product_id]))


@login_required(login_url='/shop/login')
def shop_cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')  # Bir önceki adresi alır
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Product deleted from  cart.. ")
    return HttpResponseRedirect(url)


@login_required(login_url='/shop/login')
def shop_cart_checkout(request):
    current_user = request.user
    shopcart = ShopCart.objects.all().filter(user_id=current_user.id)
    carttotal = 0
    carttax =0
    cartwithtax =0
    for rs in shopcart:
        carttotal += rs.quantity * rs.product.discount_price
        carttax = (14 / 100) * carttotal
        cartwithtax = carttotal + carttax

    form = OrderForm(request.POST or None)
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():

            # Send Credit card information to bank and get result
            # If payment accepted continue else send payment error to checkout page

            data = Order()
            data.name = form.cleaned_data['name']  # get product quantity from form
            data.surname = form.cleaned_data['surname']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.to = form.cleaned_data['name']
            data.user_id = current_user.id
            data.total = carttotal
            data.save()

            # Save Shopcart items to Order detail items
            for rs in shopcart:
                detail = OrderDetail()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                # detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.total = rs.amount
                detail.save()
                #  Reduce product Amount  (quantity)

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Order has been completed. Thank You ")
            return HttpResponseRedirect("/order")

    context = {'page': 'checkout',
               'shopcart': shopcart,
               'carttax':carttax,
               'cartwithtax':cartwithtax,
               'carttotal': carttotal,
               }
    return render(request, 'shop_cart_checkout.html', context)


@login_required(login_url='/shop/login')
def order_detail(request, id):
    order = Order.objects.get(pk=id)
    items = OrderDetail.objects.all().filter(order=id)

    context = {'page': 'detail',
               'order': order,
               'items': items,
               }
    return render(request, 'order_detail.html', context)
