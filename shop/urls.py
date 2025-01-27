
from django.urls import path
from shop import views

urlpatterns = [
path('', views.index, name='home'),
    path('<int:id>/',views.detail, name='detail'),
    path('category-product/<int:category_id>/',views.index, name='category-product'),
    path('order-detail/<int:pk>/save/', views.order_detail, name='order_detail'),
    path('comment-detail/<int:pk>/save/', views.comment_detail, name='comment_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
]
