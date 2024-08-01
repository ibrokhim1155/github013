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
    path('all-products/', views.product_list, name='index'),
    path('rating/', views.ratings, name='rating'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
