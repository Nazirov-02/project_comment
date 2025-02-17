
from django.urls import path
from shop import views

urlpatterns = [
path('', views.ProductListView.as_view(), name='home'),
    path('<int:pk>/',views.DetailProductView.as_view(), name='detail'),
    path('category-product/<int:category_id>/',views.ProductListView.as_view(), name='category-product'),
    path('order-detail/<int:pk>/save/', views.OrderCreateView.as_view(), name='order_detail'),
    path('comment-detail/<int:pk>/save/', views.CommentView.as_view(), name='comment_detail'),
    path('add-product/', views.CreateProductView.as_view(), name='add_product'),
    path('delete-product/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('edit-product/<int:pk>/', views.UpdateProductView.as_view(), name='edit_product'),
]
