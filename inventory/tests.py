from datetime import timedelta
import json
from pathlib import Path
from urllib.parse import urlsplit

from django.core import mail
from django.test import TestCase, override_settings
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

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_email_restores_expired_account(self):
        account = User.objects.create_user(
            username="emailuser",
            email="emailuser@example.com",
            password="StrongPass123!",
            role=User.Role.WORKER,
            organization=self.boss,
            credential_expires_at=timezone.now() - timedelta(days=1),
        )
        response = self.client.post(
            reverse("password_reset"), {"email": account.email}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [account.email])
        self.assertIn("/password-reset/", mail.outbox[0].body)

        reset_url = next(
            line.strip()
            for line in mail.outbox[0].body.splitlines()
            if "/password-reset/" in line
        )
        reset_response = self.client.get(urlsplit(reset_url).path)
        confirm_path = reset_response["Location"]
        self.assertEqual(self.client.get(confirm_path).status_code, 200)
        response = self.client.post(
            confirm_path,
            {
                "new_password1": "BrandNewStrongPass123!",
                "new_password2": "BrandNewStrongPass123!",
            },
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(account.credential_expires_at)
        self.assertTrue(account.check_password("BrandNewStrongPass123!"))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_email_uses_selected_english_language(self):
        account = User.objects.create_user(
            username="englishuser",
            email="englishuser@example.com",
            password="StrongPass123!",
            role=User.Role.WORKER,
            organization=self.boss,
        )
        self.client.cookies["nekezab_language"] = "en"
        self.client.post(reverse("password_reset"), {"email": account.email})

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Password reset", mail.outbox[0].subject)
        self.assertIn("You requested a password reset", mail.outbox[0].body)

    def test_service_worker_is_available_at_root_scope(self):
        response = self.client.get(reverse("service_worker"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Service-Worker-Allowed"], "/")
        self.assertIn('self.addEventListener("fetch"', response.content.decode())

    def test_pwa_manifest_has_standard_install_icons(self):
        manifest_path = (
            Path(__file__).parent
            / "static"
            / "inventory"
            / "manifest.webmanifest"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        icon_sizes = {icon["sizes"] for icon in manifest["icons"]}
        self.assertIn("192x192", icon_sizes)
        self.assertIn("512x512", icon_sizes)
