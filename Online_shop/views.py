from typing import Optional

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentModelForm, ProductModelForm, OrderModelForm
from .models import Product, Comment, Category


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'online_shop/product_list.html', context)


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
    categories = Category.objects.all()
    search = request.GET.get('search')
    if search:
        comments = Comment.objects.filter(comment__icontains=search)
    else:
        comments = Comment.objects.filter(product=_id).order_by('-created_at')[:10]
    context = {
        'categories': categories,
        'comments': comments,
        'products': related_products,
        'product': product
    }
    return render(request, 'online_shop/detail.html', context)


def add_comment(request, _id):
    product = get_object_or_404(Product, pk=_id)
    form = CommentModelForm()
    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            messages.success(request, 'Your comment has been saved.')
            return redirect('detail', _id=product.id)
    context = {
        'form': form,
    }
    return render(request, 'online_shop/detail.html', context)


def add_order(request, _id):
    product = get_object_or_404(Product, pk=_id)
    order_form = OrderModelForm()
    if request.method == 'POST':
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
                messages.error(request, 'Not enough stock availabl')
    context = {'form': order_form}
    return render(request, 'online_shop/detail.html', context)


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


def edit_product(request, _id):
    product = get_object_or_404(Product, id=_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', _id)
        else:
            return redirect('detail', _id)
    context = {
        'form': form,
    }
    return render(request, 'online_shop/edit_product.html', context)
