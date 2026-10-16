from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Product, Sale, User


class StockGuardWorkflowTests(TestCase):
    def setUp(self):
        self.boss = User.objects.create_user(
            username="boss", password="StrongPass123!", role=User.Role.BOSS
        )
        self.worker = User.objects.create_user(
            username="worker",
            password="StrongPass123!",
            role=User.Role.WORKER,
            organization=self.boss,
        )
        self.product = Product.objects.create(
            organization=self.boss,
            name="Mchele",
            purchase_price="2000.00",
            selling_price="2500.00",
            stock_quantity=5,
            low_stock_threshold=2,
        )

    def test_sale_reduces_inventory_and_uses_current_selling_price(self):
        self.client.force_login(self.worker)
        response = self.client.post(
            reverse("create_sale"),
            {"product": self.product.pk, "quantity": 2},
            follow=True,
        )
        self.product.refresh_from_db()
        sale = Sale.objects.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.stock_quantity, 3)
        self.assertEqual(sale.unit_price, self.product.selling_price)
        self.assertEqual(sale.total, 5000)
        self.assertEqual(sale.sold_by, self.worker)

    def test_sale_rejects_quantity_above_stock(self):
        self.client.force_login(self.worker)
        self.client.post(
            reverse("create_sale"),
            {"product": self.product.pk, "quantity": 6},
            follow=True,
        )
        self.product.refresh_from_db()

        self.assertEqual(self.product.stock_quantity, 5)
        self.assertFalse(Sale.objects.exists())

    def test_worker_cannot_sell_another_business_product(self):
        other_boss = User.objects.create_user(
            username="otherboss", password="StrongPass123!", role=User.Role.BOSS
        )
        other_product = Product.objects.create(
            organization=other_boss,
            name="Sukari",
            purchase_price="1000.00",
            selling_price="1500.00",
            stock_quantity=4,
        )
        self.client.force_login(self.worker)
        self.client.post(
            reverse("create_sale"),
            {"product": other_product.pk, "quantity": 1},
            follow=True,
        )

        self.assertFalse(Sale.objects.exists())

    def test_admin_superuser_is_assigned_admin_role(self):
        admin = User.objects.create_superuser(
            username="root", email="root@example.com", password="StrongPass123!"
        )

        self.assertEqual(admin.role, User.Role.ADMIN)

    def test_expired_pin_cannot_log_in(self):
        expired_user = User.objects.create_user(
            username="expired",
            password="StrongPass123!",
            role=User.Role.WORKER,
            organization=self.boss,
            credential_expires_at=timezone.now() - timedelta(seconds=1),
        )
        response = self.client.post(
            reverse("login"),
            {"username": expired_user.username, "password": "StrongPass123!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

