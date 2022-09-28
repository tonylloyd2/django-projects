from django.urls import path
from . import views as ProductViews

urlpatterns = [
    path('product-details/<product_id>/<product_name>/',ProductViews.ProductDetails,name="ProductDetails"),
    path('product-details/',ProductViews.ProductDetails,name="ProductDetails"),
    path('shop-display/',ProductViews.shop,name="shop"),
    path('shop-display/<category_id>/<category_name>/',ProductViews.CategoryShop,name="CategoryShop"),
    path('new-arrival/',ProductViews.NewArrival,name="NewArrival"),
    path('flash-sale/',ProductViews.FlashSale,name="FlashSale"),
]