from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("user/", views.user_page, name="user-page"),
    path("products/", views.products, name="products"),
    path("customer/<int:pk>/", views.customer, name="customer"),
    path("create_order/<int:pk>/", views.order_create, name="create-order"),
    path("update_order/<int:pk>/", views.order_update, name="update-order"),
    path("delete_order/<int:pk>/", views.order_delete, name="delete-order"),
]
