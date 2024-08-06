from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:_id>/', views.home, name='category'),
    path('detail/<int:_id>/', views.detail, name='detail'),
    path('product/<int:_id>/comment/', views.product_comment, name='product_comment'),
    path('product/<int:_id>/order/', views.product_order, name='product_order'),
    path('about/', views.about, name='about'),
    path('all-products/', views.product_list, name='product_list'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:_id>/', views.edit_product, name='edit_product'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
