from django.urls import path

from . import views


urlpatterns = [
    path("", views.latest_news, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('search', views.stock_search, name='stock_search'),
    path("stock/<str:symbol>", views.stock_details_view, name="stock_details"),
    path("buy_stock", views.buy_stock, name="buy_stock"),
    path("portfolio", views.portfolio_view, name="portfolio")
]