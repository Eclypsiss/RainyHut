from django.urls import path
from . import views
from .views import TableOrdersView, TableStatusView, OrderDetailViewSet, expense, update_material

urlpatterns = [
    path('dishes/', views.dishes, name='dishes'),
    path('dishes/<int:pk>/', views.dishes_detail, name='dishes_detail'),
    path('takeaway/', views.takeaway, name='takeaway'),
    path('takeaway/<int:pk>/', views.takeaway_detail, name='takeaway_detail'),
    path('order/', views.order, name='order'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('tables/<int:pk>/status/', TableStatusView.as_view(), name='table_status'),
    path('orders/<int:order_id>/', OrderDetailViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='order-detail'),
    path('expenses/', expense, name='expenses'),
    path('tables/', views.tables, name='tables'),
    path('materials/', views.materials, name='materials'),
    path('tables/<int:pk>/orders/', TableOrdersView.as_view(), name='table-orders'),
    path('materials/<int:material_id>/update/', update_material, name='update_material')
]
