from django.shortcuts import render

from accounts.models import Customer, Order, Product


def home(request):
    """Dashboard View"""
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()

    context = {
        "customers": customers,
        "orders": orders,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "orders_delivered": orders_delivered,
        "orders_pending": orders_pending,
    }

    return render(
        request=request, template_name="dashboard/index.html", context=context
    )


def products(request):
    """Products view"""
    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(
        request=request, template_name="dashboard/products.html", context=context
    )


def customer(request, pk):
    """Customer view"""
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    context = {
        "customer": customer,
        "orders": orders,
        "orders_count": orders_count,
    }

    return render(
        request=request, template_name="dashboard/customer.html", context=context
    )
