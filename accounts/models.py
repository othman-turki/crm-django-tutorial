from django.db import models


class Customer(models.Model):
    """Customer Model"""

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    """Tag Model"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Product Model"""

    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Out Door", "Out Door"),
    )

    name = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=255, choices=CATEGORY)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    """Order Model"""

    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS)

    def __str__(self):
        return f"{self.product}"
