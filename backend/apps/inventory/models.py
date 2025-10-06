from django.db import models

# ===========================
# CATEGORY & PRODUCT MODELS
# ===========================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # cost price
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)  # optional
    alert_level = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ProductInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)
    sold_today = models.PositiveIntegerField(default=0)

    def is_low_stock(self):
        return self.quantity <= self.product.alert_level

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs left"


# ===========================
# PACKAGING MODELS
# ===========================

class PackagingType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Cup, Lid, Straw, Paper Plate

    def __str__(self):
        return self.name


class PackagingVariant(models.Model):
    packaging_type = models.ForeignKey(PackagingType, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=100)  # e.g., Small, Medium, Large
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('packaging_type', 'name')

    def __str__(self):
        return f"{self.packaging_type.name} ({self.name})"


class PackagingInventory(models.Model):
    packaging_variant = models.OneToOneField(PackagingVariant, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)
    alert_level = models.PositiveIntegerField(default=20)

    def is_low_stock(self):
        return self.quantity <= self.alert_level

    def __str__(self):
        return f"{self.packaging_variant} - {self.quantity} pcs left"


# ===========================
# DAMAGED PACKAGING
# ===========================

class DamagedPackaging(models.Model):
    packaging_variant = models.ForeignKey(PackagingVariant, on_delete=models.CASCADE, related_name="damaged")
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.packaging_variant} - {self.quantity} damaged"


# ===========================
# RESTOCK RECORD
# ===========================

class RestockRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    packaging_variant = models.ForeignKey(PackagingVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity_added = models.PositiveIntegerField()
    date_restocked = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        target = self.product.name if self.product else self.packaging_variant.name
        return f"Restocked {target} ({self.quantity_added})"
