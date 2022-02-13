from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import Customer, Order, Product
from .forms import CreateUserForm, OrderForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def register(request):
    """Register View"""

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="customer")
            user.groups.add(group)

            username = form.cleaned_data.get("username")
            messages.success(
                request=request, message=f"Account was created for {username}"
            )

            return redirect("accounts:login")

    form = CreateUserForm()

    context = {"form": form}
    return render(
        request=request, template_name="accounts/register.html", context=context
    )


@unauthenticated_user
def log_in(request):
    """Login View"""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)

            return redirect("accounts:home")

        else:
            messages.info(request=request, message="Incorrect Credenials")

    context = {}
    return render(request=request, template_name="accounts/login.html", context=context)


def log_out(request):
    """Logout View"""
    logout(request=request)

    return redirect("accounts:login")


@login_required(login_url="accounts:login")
@admin_only
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


@login_required(login_url="accounts:login")
def user_page(request):
    context = {}

    return render(request=request, template_name="dashboard/user.html", context=context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=["admin"])
def products(request):
    """Products view"""
    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(
        request=request, template_name="dashboard/products.html", context=context
    )


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):
    """Customer view"""
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {
        "customer": customer,
        "orders": orders,
        "orders_count": orders_count,
        "order_filter": order_filter,
    }

    return render(
        request=request, template_name="dashboard/customer.html", context=context
    )


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=["admin"])
def order_create(request, pk):
    """Create Order View"""

    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=6
    )

    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()

            return redirect("accounts:home")

    # form = OrderForm(initial={"customer": customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    context = {
        "formset": formset,
    }

    return render(
        request=request, template_name="dashboard/order_form.html", context=context
    )


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=["admin"])
def order_update(request, pk):
    """Update Order View"""

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()

            return redirect("accounts:home")

    form = OrderForm(instance=order)

    context = {
        "form": form,
    }

    return render(
        request=request, template_name="dashboard/order_form.html", context=context
    )


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=["admin"])
def order_delete(request, pk):
    """Delete Order View"""

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()

        return redirect("accounts:home")

    context = {"order": order}

    return render(
        request=request, template_name="dashboard/delete.html", context=context
    )
