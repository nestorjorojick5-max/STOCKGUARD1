from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("stock/add/", views.add_stock, name="add_stock"),
    path("sales/new/", views.create_sale, name="create_sale"),
    path("reports/", views.reports, name="reports"),
    path("reports/pdf/", views.report_pdf, name="report_pdf"),
    path("users/", views.users, name="users"),
    path("users/<int:user_id>/reset-pin/", views.reset_pin, name="reset_pin"),
    path("users/<int:user_id>/toggle/", views.toggle_user, name="toggle_user"),
    path("settings/", views.settings_page, name="settings"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
