from itertools import product
from django.contrib import admin
from .models import Product,Category,ProductImage, RatingReview

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(RatingReview)
