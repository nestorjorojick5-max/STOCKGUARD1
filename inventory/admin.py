from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Product, Sale, StockEntry, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "role",
        "organization",
        "is_active",
        "credential_expires_at",
    )
    list_filter = ("role", "is_active")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("StockGuard", {"fields": ("role", "organization", "credential_expires_at")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("StockGuard", {"fields": ("role", "organization")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "stock_quantity", "selling_price")
    list_filter = ("organization",)
    search_fields = ("name", "organization__username")


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ("product", "organization", "quantity", "unit_cost", "recorded_by", "recorded_at")
    list_filter = ("organization", "recorded_at")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("product", "organization", "quantity", "unit_price", "sold_by", "sold_at")
    list_filter = ("organization", "sold_at")
