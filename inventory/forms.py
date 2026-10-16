from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from .models import Product, Sale, StockEntry, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Jina la mtumiaji",
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )
    password = forms.CharField(
        label="PIN / Nenosiri",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if (
            user.credential_expires_at
            and user.credential_expires_at <= timezone.now()
        ):
            raise forms.ValidationError(
                "Muda wa PIN umeisha. Tafadhali wasiliana na msimamizi wako.",
                code="expired_credential",
            )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "purchase_price",
            "selling_price",
            "stock_quantity",
            "low_stock_threshold",
        )
        labels = {
            "name": "Jina la bidhaa",
            "purchase_price": "Bei ya kununulia (TSh)",
            "selling_price": "Bei ya kuuza (TSh)",
            "stock_quantity": "Idadi ya kuanzia",
            "low_stock_threshold": "Tahadhari ya stock ikifika",
        }
        widgets = {
            "purchase_price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "selling_price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "stock_quantity": forms.NumberInput(attrs={"min": "0"}),
            "low_stock_threshold": forms.NumberInput(attrs={"min": "0"}),
        }


class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ("product", "quantity", "unit_cost")
        labels = {
            "product": "Bidhaa",
            "quantity": "Idadi iliyonunuliwa",
            "unit_cost": "Bei ya kununulia kwa moja (TSh)",
        }
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": "1"}),
            "unit_cost": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ("product", "quantity")
        labels = {"product": "Bidhaa", "quantity": "Idadi ya kuuza"}
        widgets = {"quantity": forms.NumberInput(attrs={"min": "1"})}


class ManagedUserForm(forms.Form):
    username = forms.CharField(
        label="Jina la mtumiaji",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Jina hili tayari linatumika.")
        return username


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Nenosiri la sasa", widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label="Nenosiri jipya",
        widget=forms.PasswordInput,
        validators=[validate_password],
    )
    confirm_password = forms.CharField(
        label="Rudia nenosiri jipya", widget=forms.PasswordInput
    )

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Nenosiri la sasa si sahihi.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get("new_password")
            and cleaned_data.get("confirm_password")
            and cleaned_data["new_password"] != cleaned_data["confirm_password"]
        ):
            self.add_error("confirm_password", "Nenosiri ulilorudia halifanani.")
        return cleaned_data
