from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentModelForm, OrderModelForm, ProductModelForm
from .models import Product, Comment, Category
from django.contrib import messages
from django.db.models import Avg
from typing import Optional


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'online_shop/product_list.html', context)


def cheap(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('price')
    context = {'categories': categories, 'products': products}
    return render(request, 'online_shop/home.html', context)


def home(request, _id: Optional[int] = None):
    if _id:
        products = Product.objects.filter(category=_id)
    else:
        products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'online_shop/home.html', context)


def detail(request, _id):
    product = get_object_or_404(Product, pk=_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=_id)
    comments = Comment.objects.filter(product=_id).order_by('-created_at')[:3]
    categories = Category.objects.all()
    new_comment = None
    new_order = None
    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        order_form = OrderModelForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            messages.success(request, 'Your comment has been saved.')
            return redirect('detail', _id=product.id)
        if order_form.is_valid():
            quantity = order_form.cleaned_data['quantity']
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()

                new_order = order_form.save(commit=False)
                new_order.product = product
                new_order.save()
                messages.success(request, 'Your order has been submitted!')
                return redirect('detail', _id=_id)
            else:
                messages.error(request, 'Not enough stock availabl'
                                        'e.')
    context = {
        'new_comment': new_comment,
        'new_order': new_order,
        'categories': categories,
        'comments': comments,
        'products': related_products,
        'product': product
    }
    return render(request, 'online_shop/detail.html', context)


def expensive(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-price')
    context = {'categories': categories, 'products': products}
    return render(request, 'online_shop/home.html', context)


def ratings(request):
    products = Product.objects.annotate(average_rating=Avg('rating')).order_by('-average_rating')
    context = {'products': products}
    return render(request, 'online_shop/ratings.html', context)


def about(request):
    return render(request, 'online_shop/about.html')


def product_comment(request, _id):
    product = get_object_or_404(Product, id=_id)
    return render(request, 'online_shop/detail.html', {'product': product})


def product_order(request, _id):
    product = get_object_or_404(Product, id=_id)
    return render(request, 'online_shop/detail.html', {'product': product})


def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {
        'form': form
    }
    return render(request, 'online_shop/add_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return redirect('home')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('detail', product_id)
    context = {
        'form': form,
        'product': product

    }
    return render(request, 'online_shop/edit_product.html', context)
