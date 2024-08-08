
from django.contrib import admin
from Online_shop.models import Product, Category, Comment, Order

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Comment)
# admin.site.register(Order)
# unregister(User)

class IsVeryExpensiveFilter(admin.SimpleListFilter):
    title = 'Is Very Expensive Product'
    parameter_name = 'is_very_expensive_product'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(price__gt=20_000)
        elif value == 'No':
            return queryset.exclude(price__gt=20_000)
        return queryset


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    # def product_count(self, obj):
    #     return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'discount', 'get_image_url', 'is_very_expensive_product')
    search_fields = ['name']
    list_filter = ['category', IsVeryExpensiveFilter]

    def is_very_expensive_product(self, obj):
        return obj.price > 20_000

    is_very_expensive_product.boolean = True



@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'comment')
    search_fields = ['product']
    list_filter = ['product']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')
    search_fields = ['product']
    list_filter = ['product']
