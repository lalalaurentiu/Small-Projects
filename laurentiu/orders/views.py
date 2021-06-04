from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm
from cart.cart import Cart
from django.views import View
from shop.models import Product
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.

class Order_Create(View):

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        product = Product.objects.all()
        return render(request, 'orders/order/create.html', {'cart': cart,
                                                            'product': product,
                                                            'form': form})


    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

           
            cart.clear()
            
            request.session['order_id'] = order.id
            
            return render(request, 'orders/order/created.html')


class Admin_Order_Detail(View):

        def get(self, request, order_id):
            order = get_object_or_404(Order, id=order_id)
            return render(request, 'admin/orders/order/detail.html', {'order': order})


        def post(self, request):
            pass

