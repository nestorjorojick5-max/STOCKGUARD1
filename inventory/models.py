from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.db.models import Q
from django.utils import timezone


class UserManager(DjangoUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        BOSS = "boss", "Boss"
        WORKER = "worker", "Worker"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.WORKER)
    organization = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="team_members",
        limit_choices_to={"role": Role.BOSS},
    )
    credential_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role == self.Role.BOSS:
            self.organization = None
        super().save(*args, **kwargs)

    @property
    def is_credential_expired(self):
        return bool(
            self.credential_expires_at
            and self.credential_expires_at <= timezone.now()
        )


class Product(models.Model):
    organization = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=120)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="unique_product_per_shop"
            ),
            models.CheckConstraint(
                condition=Q(purchase_price__gte=0) & Q(selling_price__gte=0),
                name="product_prices_nonnegative",
            ),
        ]

    def __str__(self):
        return self.name


class StockEntry(models.Model):
    organization = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stock_entries"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="stock_entries"
    )
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="recorded_stock_entries"
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    @property
    def total_cost(self):
        return self.quantity * self.unit_cost


class Sale(models.Model):
    organization = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_sales"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="sales")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    sold_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sales")
    sold_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sold_at"]

    @property
    def total(self):
        return self.quantity * self.unit_price
