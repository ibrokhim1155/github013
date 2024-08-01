from django.contrib import admin

from Online_shop.models import Product, Category, Comment, Order

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Order)