from django.contrib import admin
from .models import SiteUser, Products, ProductCategory,ProductImage, Auction_Details
# from .models import Products
# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(SiteUser)
admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(Auction_Details)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'category', 'initial_price', 'created_at', 'updated_at', 'auction_start_time', 'auction_end_time')
#     readonly_fields = ('auction_start_time', 'auction_end_time')

#     def auction_start_time(self, obj):
#         if obj.auction_details:
#             return obj.auction_details.start_time
#         return None

#     def auction_end_time(self, obj):
#         if obj.auction_details:
#             return obj.auction_details.end_time
#         return None

# admin.site.register(Products, ProductAdmin)