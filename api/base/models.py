from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isVerified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return self.user.username

class ProductCategory(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=500)
   
    def __str__(self):
        return self.title

class Products(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.image}'
    
class Auction_Details(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    def clean(self):
        # Check if the end time is at least 15 minutes greater than the start time
        if self.end_time <= self.start_time + timezone.timedelta(minutes=15):
            raise ValidationError("End time must be at least 15 minutes greater than the start time.")
        
        # Check if the product is already in an active auction
        active_auctions = Auction_Details.objects.filter(product=self.product, end_time__gt=timezone.now())
        if active_auctions.exists():
            raise ValidationError("This product is already in an active auction.")
    
class Bids(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_bids')
    bidder = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.bidder.user.username} - {self.price}"
    
    def clean(self):
        # Check if the product is listed in Auction_Details
        if not Auction_Details.objects.filter(product=self.product).exists():
            raise ValidationError("This product is not listed in Auction_Details.")
        
        # Check if the updated price is greater than the current price
        if self.id:
            current_price = Bids.objects.get(id=self.id).price
            if self.price <= current_price:
                raise ValidationError("Updated price must be greater than the current price.")


class WinningBid(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE, related_name='winning_bid')
    bid = models.OneToOneField(Bids, on_delete=models.CASCADE)
    won_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"Winner of {self.product.name}"
