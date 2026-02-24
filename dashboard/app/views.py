from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import json
import csv

from .models import Product, Category, Sale, SaleItem, ActivityLog
from .forms import ProductForm


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):

    total_sales = Sale.objects.count()

    total_revenue = Sale.objects.aggregate(
        revenue=Sum('total_amount')
    )['revenue'] or 0

    total_profit = SaleItem.objects.aggregate(
        profit=Sum(
            ExpressionWrapper(
                (F('product__selling_price') - F('product__purchase_price')) * F('quantity'),
                output_field=DecimalField()
            )
        )
    )['profit'] or 0

    monthly_revenue_data = (
        Sale.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'))
        .order_by('month')
    )

    revenue_months = [entry['month'].strftime('%b %Y') for entry in monthly_revenue_data]
    revenue_totals = [float(entry['revenue']) for entry in monthly_revenue_data]

    monthly_profit_data = (
        SaleItem.objects
        .annotate(month=TruncMonth('sale__created_at'))
        .values('month')
        .annotate(
            profit=Sum(
                ExpressionWrapper(
                    (F('product__selling_price') - F('product__purchase_price')) * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )
        .order_by('month')
    )

    profit_months = [entry['month'].strftime('%b %Y') for entry in monthly_profit_data]
    profit_totals = [float(entry['profit']) for entry in monthly_profit_data]

    low_stock = Product.objects.filter(quantity__lte=5).count()
    total_products = Product.objects.count()
    in_stock = total_products - low_stock

    context = {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'revenue_months': json.dumps(revenue_months),
        'revenue_totals': json.dumps(revenue_totals),
        'profit_months': json.dumps(profit_months),
        'profit_totals': json.dumps(profit_totals),
        'low_stock': low_stock,
        'in_stock': in_stock,
    }

    return render(request, 'dashboard.html', context)


# =========================
# PRODUCTS
# =========================

@login_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })


@login_required
def product_add(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    form = ProductForm(request.POST or None)
    if form.is_valid():
        product = form.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Created product: {product.name}"
        )

        return redirect('product_list')

    return render(request, 'products/product_form.html', {'form': form})


@login_required
def product_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')

    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        updated_product = form.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Updated product: {updated_product.name}"
        )

        return redirect('product_list')

    return render(request, 'products/product_form.html', {'form': form})


@login_required
def product_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')

    product = get_object_or_404(Product, pk=pk)

    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted product: {product.name}"
    )

    product.delete()
    return redirect('product_list')


# =========================
# SALES
# =========================

@login_required
def create_sale(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        with transaction.atomic():
            sale = Sale.objects.create()
            total_amount = 0

            for product_id, qty in zip(product_ids, quantities):
                product = Product.objects.get(id=product_id)
                qty = int(qty)

                if qty > 0:
                    if product.quantity < qty:
                        return render(request, 'sales/create_sale.html', {
                            'products': products,
                            'error': f"Not enough stock for {product.name}"
                        })

                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=qty,
                        price=product.selling_price
                    )

                    product.quantity -= qty
                    product.save()

                    total_amount += product.selling_price * qty

            sale.total_amount = total_amount
            sale.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Created sale ID: {sale.id}"
            )

            # =====================
            # SEND EMAIL INVOICE
            # =====================

            subject = f"Invoice for Sale #{sale.id}"

            message = f"""
Thank you for your purchase!Stock is low..

Sale ID: {sale.id}
Date: {sale.created_at.strftime('%Y-%m-%d')}
Total Amount: ₹{sale.total_amount}

Regards,
Stock Manager
"""

            recipient = request.user.email if request.user.email else settings.EMAIL_HOST_USER

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=True,
            )

        return redirect('sale_list')

    return render(request, 'sales/create_sale.html', {'products': products})


@login_required
def sale_list(request):
    sales = Sale.objects.all().order_by('-created_at')
    return render(request, 'sales/sale_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


# =========================
# EXPORT CSV
# =========================

@login_required
def export_sales_csv(request):

    if not request.user.is_superuser:
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Sale ID',
        'Date',
        'Product',
        'Quantity',
        'Selling Price',
        'Total',
        'Profit'
    ])

    sale_items = SaleItem.objects.select_related('sale', 'product')

    for item in sale_items:
        profit = (item.product.selling_price - item.product.purchase_price) * item.quantity

        writer.writerow([
            item.sale.id,
            item.sale.created_at.strftime('%Y-%m-%d'),
            item.product.name,
            item.quantity,
            item.product.selling_price,
            item.get_total(),
            profit
        ])

    return response


# =========================
# ACTIVITY LOGS
# =========================

@login_required
def activity_logs(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'activity_logs.html', {'logs': logs})


# =========================
# SIGNUP
# =========================

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        login(request, user)
        return redirect('dashboard')

    return render(request, 'signup.html')