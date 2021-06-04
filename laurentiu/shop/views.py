from django.shortcuts import render, get_object_or_404
from .models import Category, Product 
from cart.forms import CartAddProductForm
from cart.cart import Cart
# Create your views here.

def categories(request, category_slug = None):
    categories = Category.objects.all()
    category_name = None
    cart = Cart(request)
    if category_slug:
        category_name = get_object_or_404(Category, slug=category_slug)
    return render(request, 'shop/products/main_page.html', {
                                    'category': category_name, 
                                    'categories': categories,
                                    'cart':cart})

def product_list(request, category_slug = None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    category_name = None
    if category_slug:
        category_name = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category_name)
    return render(request, 'shop/products/list.html',{'products':products,
                            'category':category_name,
                            'categories':categories,
                            'cart':cart})

def product_detail(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/products/detail.html', {'product': product, 'cart_product_form': cart_product_form })
    