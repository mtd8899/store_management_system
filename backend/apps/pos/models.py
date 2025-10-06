from django.db import models
from django.contrib.auth.models import User
# from inventory.models import Product  # import your Product model

class Sale(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('partial_returned', 'Partial Returned'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ]

    date = models.DateTimeField(auto_now_add=True)                              
    made_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_made')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')                                           
    
    def __str__(self):
        return f"Sale {self.id} by {self.made_by.username if self.made_by else 'Unknown'}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items')
   # product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)                                                          
    quantity = models.PositiveIntegerField()                                                                  
    returned_quantity = models.PositiveIntegerField(default=0)
    return_reason = models.TextField(null=True, blank=True)
    
    #def __str__(self):
     #   return f"{self.quantity} x {self.product.name if self.product else 'Unknown'}"


class SaleCancellation(models.Model):                                                                                  
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='cancellations')                                                                                                         
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)                                                                                                            
    reason = models.TextField()                                                                                                                 
    date_cancelled = models.DateTimeField(auto_now_add=True)
                                                                                                                    
    def __str__(self):                                                                                                          
        return f"Sale {self.sale.id} cancelled on {self.date_cancelled}"                                       
    
    
class PurchaseReturn(models.Model):                                                                                                                                
    reference = models.CharField(max_length=255)                                                                                                                                    
    date = models.DateTimeField(auto_now_add=True)
