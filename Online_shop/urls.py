from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from Online_shop import auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:_id>/', views.home, name='category'),
    path('detail/<int:_id>/', views.detail, name='detail'),
    path('product/<int:_id>/comment/', views.add_comment, name='product_comment'),
    path('product/<int:_id>/order/', views.add_order, name='product_order'),
    path('about/', views.about, name='about'),
    path('all-products/', views.product_list, name='product_list'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:_id>/', views.edit_product, name='edit_product'),
    path('login/', auth_views.login_user, name='login_page'),
    path('login/', auth_views.login_user, name='login'),
    path('logout/', auth_views.logout_user, name='logout_page'),
    path('logout/', auth_views.logout_user, name='logout'),
    path('register/', auth_views.register_user, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
