from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product

def home(request):
    featured_products = Product.objects.all()[:3]

    cart = request.session.get('cart', [])

    return render(request, "home.html", {
        "featured_products": featured_products,
        "cart_count": len(cart)
    })


def index(request):
    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    cart = request.session.get('cart', [])

    return render(request, 'index.html', {
        'products': products,
        'cart_count': len(cart)
    })


def new(request):
    return HttpResponse('Welcome to PyShop New Arrivals')


# Show cart page
def cart(request):
    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    total = sum(product.price for product in products)

    return render(request, 'cart.html', {
        'products': products,
        'total': total,
        'cart_count': len(cart)
    })
# Add product to cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('products:cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('products:cart')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', [])

    return render(request, 'product_detail.html', {
        'product': product,
        'cart_count': len(cart)
    })