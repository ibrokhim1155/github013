from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    products = Product.objects.filter(category=_id) if _id else Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'online_shop/home.html', context)


def detail(request, _id):
    product = get_object_or_404(Product, pk=_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=_id)
    categories = Category.objects.all()
    search = request.GET.get('search')
    comments = Comment.objects.filter(comment__icontains=search) if search else Comment.objects.filter(
        product=_id).order_by('-created_at')[:10]
    context = {
        'categories': categories,
        'comments': comments,
        'products': related_products,
        'product': product
    }
    return render(request, 'online_shop/detail.html', context)


def add_comment(request, _id):
    product = get_object_or_404(Product, pk=_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            messages.success(request, 'Your comment has been saved.')
            return redirect('detail', _id=product.id)
    else:
        form = CommentModelForm()

    context = {'form': form}
    return render(request, 'online_shop/detail.html', context)


@login_required(login_url='register')
def add_order(request, product_slug: Optional[str] = None):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            if product.quantity >= int(form.cleaned_data['quantity']):
                product.quantity -= int(form.cleaned_data['quantity'])
                product.save()
                order = form.save(commit=False)
                order.product = product
                order.save()
                messages.success(request, 'Your order has been submitted!')
                return redirect('detail', product.slug)
            messages.error(request, 'Not enough stock available.')
    else:
        form = OrderModelForm()

    context = {'form': form, 'product': product}
    return render(request, 'online_shop/detail.html', context)


@login_required(login_url='register')
def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your product has been added.')
            return redirect('home')
        messages.error(request, 'Something went wrong!')
    else:
        form = ProductModelForm()

    context = {'form': form}
    return render(request, 'online_shop/add_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return redirect('home')


def edit_product(request, _id):
    product = get_object_or_404(Product, id=_id)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated.')
            return redirect('detail', _id=product.id)
    else:
        form = ProductModelForm(instance=product)

    context = {'form': form}
    return render(request, 'online_shop/edit_product.html', context)


def about(request):
    return render(request, 'online_shop/about.html')
