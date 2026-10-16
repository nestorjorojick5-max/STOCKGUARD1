import secrets
from calendar import monthrange
from datetime import datetime, time, timedelta
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.db import IntegrityError, transaction
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph

from .forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    LoginForm,
    ManagedUserForm,
    ProductForm,
    SaleForm,
    StockEntryForm,
)
from .models import Product, Sale, User


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


class CredentialResetConfirmView(DjangoPasswordResetConfirmView):
    def form_valid(self, form):
        self.user.credential_expires_at = None
        self.user.save(update_fields=["credential_expires_at"])
        return super().form_valid(form)


class BilingualPasswordResetView(DjangoPasswordResetView):
    def form_valid(self, form):
        if self.request.COOKIES.get("nekezab_language") == "en":
            self.email_template_name = "registration/password_reset_email_en.html"
            self.subject_template_name = (
                "registration/password_reset_subject_en.txt"
            )
        return super().form_valid(form)


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def service_worker(request):
    worker_path = (
        Path(__file__).parent
        / "static"
        / "inventory"
        / "js"
        / "service-worker.js"
    )
    response = HttpResponse(
        worker_path.read_text(encoding="utf-8"),
        content_type="application/javascript; charset=utf-8",
    )
    response["Cache-Control"] = "no-cache"
    response["Service-Worker-Allowed"] = "/"
    return response


def organization_for(user):
    if user.role == User.Role.BOSS:
        return user
    return user.organization


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role == User.Role.ADMIN:
        return render(
            request,
            "inventory/admin_dashboard.html",
            {
                "bosses": User.objects.filter(role=User.Role.BOSS).order_by("username"),
                "boss_count": User.objects.filter(role=User.Role.BOSS).count(),
                "worker_count": User.objects.filter(role=User.Role.WORKER).count(),
            },
        )

    organization = organization_for(request.user)
    if organization is None:
        messages.error(request, "Akaunti hii haijaunganishwa na biashara.")
        return render(request, "inventory/dashboard.html", {"setup_error": True})

    today = timezone.localdate()
    sales_today = Sale.objects.filter(organization=organization, sold_at__date=today)
    revenue_today = sum((sale.total for sale in sales_today), Decimal("0"))
    products = Product.objects.filter(organization=organization)
    return render(
        request,
        "inventory/dashboard.html",
        {
            "organization": organization,
            "product_count": products.count(),
            "stock_count": products.aggregate(total=Sum("stock_quantity"))["total"] or 0,
            "revenue_today": revenue_today,
            "sales_count": sales_today.count(),
            "low_stock_products": products.filter(
                stock_quantity__lte=F("low_stock_threshold")
            )[:5],
            "recent_sales": Sale.objects.filter(organization=organization)[:6],
            "available_products": products.filter(stock_quantity__gt=0),
        },
    )


def boss_required(user):
    return user.role in (User.Role.BOSS, User.Role.ADMIN)


def products(request):
    if not request.user.is_authenticated:
        return redirect("login")
    organization = organization_for(request.user)
    if organization is None:
        messages.error(request, "Akaunti hii haina biashara iliyounganishwa.")
        return redirect("dashboard")
    if request.method == "POST":
        if not boss_required(request.user):
            messages.error(request, "Ni Boss pekee anayeweza kuongeza bidhaa.")
            return redirect("products")
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.organization = organization
            try:
                product.save()
            except IntegrityError:
                form.add_error("name", "Bidhaa yenye jina hili tayari ipo.")
            else:
                messages.success(request, "Bidhaa imeongezwa kwenye stock.")
                return redirect("products")
    else:
        form = ProductForm()
    return render(
        request,
        "inventory/products.html",
        {
            "products": Product.objects.filter(organization=organization),
            "form": form,
            "can_manage": boss_required(request.user),
        },
    )


@login_required
@require_POST
def add_stock(request):
    if not boss_required(request.user):
        messages.error(request, "Ni Boss pekee anayeweza kuongeza stock.")
        return redirect("products")
    organization = organization_for(request.user)
    form = StockEntryForm(request.POST)
    form.fields["product"].queryset = Product.objects.filter(organization=organization)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.organization = organization
        entry.recorded_by = request.user
        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update(),
                pk=entry.product_id,
                organization=organization,
            )
            product.stock_quantity = F("stock_quantity") + entry.quantity
            product.purchase_price = entry.unit_cost
            product.save(update_fields=["stock_quantity", "purchase_price"])
            entry.save()
        messages.success(request, "Stock imeongezwa na gharama imerekodiwa.")
    else:
        messages.error(request, "Taarifa za kuongeza stock si sahihi.")
    return redirect("products")


@login_required
@require_POST
def create_sale(request):
    organization = organization_for(request.user)
    form = SaleForm(request.POST)
    if organization is None:
        messages.error(request, "Akaunti hii haina biashara iliyounganishwa.")
        return redirect("dashboard")
    form.fields["product"].queryset = Product.objects.filter(organization=organization)
    if form.is_valid():
        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update(),
                pk=form.cleaned_data["product"].pk,
                organization=organization,
            )
            quantity = form.cleaned_data["quantity"]
            if product.stock_quantity < quantity:
                messages.error(
                    request, f"Stock haitoshi. Zilizopo: {product.stock_quantity}."
                )
            else:
                Sale.objects.create(
                    organization=organization,
                    product=product,
                    quantity=quantity,
                    unit_price=product.selling_price,
                    sold_by=request.user,
                )
                product.stock_quantity = F("stock_quantity") - quantity
                product.save(update_fields=["stock_quantity"])
                messages.success(request, "Mauzo yamehifadhiwa; stock imepungua.")
                return redirect("dashboard")
    else:
        messages.error(request, "Taarifa za mauzo si sahihi.")
    return redirect("dashboard")


def _report_period(request):
    today = timezone.localdate()
    period = request.GET.get("period", "day")
    language = request.COOKIES.get("nekezab_language", "sw")
    if period not in ("day", "month"):
        period = "day"
    if period == "month":
        selected = today.replace(day=1)
        start = timezone.make_aware(datetime.combine(selected, time.min))
        end_day = monthrange(selected.year, selected.month)[1]
        end = timezone.make_aware(
            datetime.combine(selected.replace(day=end_day) + timedelta(days=1), time.min)
        )
        if language == "en":
            label = selected.strftime("%B %Y")
        else:
            swahili_months = (
                "Januari",
                "Februari",
                "Machi",
                "Aprili",
                "Mei",
                "Juni",
                "Julai",
                "Agosti",
                "Septemba",
                "Oktoba",
                "Novemba",
                "Desemba",
            )
            label = f"{swahili_months[selected.month - 1]} {selected.year}"
    else:
        selected = today
        start = timezone.make_aware(datetime.combine(selected, time.min))
        end = start + timedelta(days=1)
        label = selected.strftime("%d/%m/%Y")
    return period, start, end, label


@login_required
def reports(request):
    organization = organization_for(request.user)
    if organization is None:
        messages.error(request, "Akaunti hii haina biashara iliyounganishwa.")
        return redirect("dashboard")
    period, start, end, label = _report_period(request)
    sales = Sale.objects.filter(
        organization=organization, sold_at__gte=start, sold_at__lt=end
    ).select_related("product", "sold_by")
    total = sum((sale.total for sale in sales), Decimal("0"))
    return render(
        request,
        "inventory/reports.html",
        {
            "sales": sales,
            "period": period,
            "label": label,
            "total": total,
            "quantity_total": sum(sale.quantity for sale in sales),
        },
    )


@login_required
def report_pdf(request):
    organization = organization_for(request.user)
    if organization is None:
        messages.error(request, "Akaunti hii haina biashara iliyounganishwa.")
        return redirect("dashboard")
    period, start, end, label = _report_period(request)
    sales = Sale.objects.filter(
        organization=organization, sold_at__gte=start, sold_at__lt=end
    ).select_related("product", "sold_by")
    english_report = request.COOKIES.get("nekezab_language") == "en"
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    rows = [
        (
            ["Time", "Product", "Qty", "Unit price (TSh)", "Total (TSh)", "Worker"]
            if english_report
            else ["Muda", "Bidhaa", "Idadi", "Bei (TSh)", "Jumla (TSh)", "Mfanyakazi"]
        )
    ]
    for sale in sales:
        rows.append(
            [
                timezone.localtime(sale.sold_at).strftime("%H:%M"),
                sale.product.name,
                str(sale.quantity),
                f"{sale.unit_price:,.2f}",
                f"{sale.total:,.2f}",
                sale.sold_by.username,
            ]
        )
    total = sum((sale.total for sale in sales), Decimal("0"))
    rows.append(
        ["", "", "", "TOTAL" if english_report else "JUMLA", f"{total:,.2f}", ""]
    )
    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d6dce5")),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#eef3fb")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    document.build(
        [
            Paragraph(
                "NEKEZA B — Sales report"
                if english_report
                else "NEKEZA B — Ripoti ya mauzo",
                styles["Title"],
            ),
            Paragraph(f"{organization.username} · {label}", styles["Normal"]),
            Spacer(1, 14),
            table,
        ]
    )
    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ripoti-{period}.pdf"'
    return response


@login_required
def users(request):
    if request.user.role not in (User.Role.ADMIN, User.Role.BOSS):
        messages.error(request, "Huna ruhusa ya kusimamia akaunti.")
        return redirect("dashboard")

    is_admin = request.user.role == User.Role.ADMIN
    target_role = User.Role.BOSS if is_admin else User.Role.WORKER
    form = ManagedUserForm(request.POST or None)
    new_pin = None
    if request.method == "POST" and form.is_valid():
        new_pin = _create_pin()
        managed = User(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            role=target_role,
            organization=None if is_admin else request.user,
            credential_expires_at=timezone.now() + timedelta(days=30),
            is_active=True,
        )
        managed.set_password(new_pin)
        managed.save()
        messages.success(
            request,
            f"Akaunti ya {managed.username} imetengenezwa. Hifadhi PIN iliyoonyeshwa hapa.",
        )
        form = ManagedUserForm()

    if is_admin:
        managed_users = User.objects.filter(role=User.Role.BOSS)
    else:
        managed_users = User.objects.filter(
            role=User.Role.WORKER, organization=request.user
        )
    return render(
        request,
        "inventory/users.html",
        {
            "users": managed_users.order_by("username"),
            "form": form,
            "new_pin": new_pin,
            "target_role": target_role,
        },
    )


def _create_pin():
    return f"{secrets.randbelow(100_000_000):08d}"


@login_required
@require_POST
def reset_pin(request, user_id):
    if request.user.role not in (User.Role.ADMIN, User.Role.BOSS):
        messages.error(request, "Huna ruhusa ya kubadilisha PIN.")
        return redirect("dashboard")
    managed = get_object_or_404(User, pk=user_id)
    if request.user.role == User.Role.ADMIN:
        permitted = managed.role == User.Role.BOSS
    else:
        permitted = managed.role == User.Role.WORKER and managed.organization_id == request.user.id
    if not permitted:
        messages.error(request, "Huna ruhusa ya kusimamia akaunti hii.")
        return redirect("users")
    new_pin = _create_pin()
    managed.set_password(new_pin)
    managed.credential_expires_at = timezone.now() + timedelta(days=30)
    managed.save(update_fields=["password", "credential_expires_at"])
    messages.success(request, f"PIN mpya ya {managed.username}: {new_pin}")
    return redirect("users")


@login_required
@require_POST
def toggle_user(request, user_id):
    if request.user.role not in (User.Role.ADMIN, User.Role.BOSS):
        messages.error(request, "Huna ruhusa ya kubadilisha akaunti.")
        return redirect("dashboard")
    managed = get_object_or_404(User, pk=user_id)
    if request.user.role == User.Role.ADMIN:
        permitted = managed.role == User.Role.BOSS
    else:
        permitted = managed.role == User.Role.WORKER and managed.organization_id == request.user.id
    if not permitted:
        messages.error(request, "Huna ruhusa ya kusimamia akaunti hii.")
        return redirect("users")
    managed.is_active = not managed.is_active
    managed.save(update_fields=["is_active"])
    messages.success(
        request,
        f"Akaunti ya {managed.username} "
        f"{'imewashwa' if managed.is_active else 'imesitishwa'}.",
    )
    return redirect("users")


@login_required
def settings_page(request):
    password_form = ChangePasswordForm(
        request.POST if request.POST.get("action") == "password" else None,
        user=request.user,
    )
    email_form = ChangeEmailForm(
        request.POST if request.POST.get("action") == "email" else None,
        user=request.user,
    )
    if request.method == "POST" and request.POST.get("action") == "password":
        if password_form.is_valid():
            request.user.set_password(password_form.cleaned_data["new_password"])
            request.user.credential_expires_at = None
            request.user.save(update_fields=["password", "credential_expires_at"])
            update_session_auth_hash(request, request.user)
            messages.success(request, "Nenosiri limebadilishwa kikamilifu.")
            return redirect("settings")
    elif request.method == "POST" and request.POST.get("action") == "email":
        if email_form.is_valid():
            request.user.email = email_form.cleaned_data["email"]
            request.user.save(update_fields=["email"])
            messages.success(
                request, "Anwani ya barua pepe imehifadhiwa kwa akaunti yako."
            )
            return redirect("settings")
    return render(
        request,
        "inventory/settings.html",
        {"password_form": password_form, "email_form": email_form},
    )


@login_required
def about(request):
    return render(request, "inventory/info.html", {"title": "Kuhusu NEKEZA B"})


@login_required
def contact(request):
    return render(
        request, "inventory/info.html", {"title": "Wasiliana na msimamizi"}
    )
