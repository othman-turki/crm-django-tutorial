from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("customer/<int:pk>/", views.customer, name="customer"),
    path("create_order/", views.order_create, name="create-order"),
    path("update_order/<int:pk>/", views.order_update, name="update-order"),
    path("delete_order/<int:pk>/", views.order_delete, name="delete-order"),
]
