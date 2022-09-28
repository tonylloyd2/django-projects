from django.urls import path
from . import views as OrderViews

urlpatterns = [
    path('view-cart/',OrderViews.ViewCart,name="ViewCart"),
    path('add-cart/',OrderViews.AddCart,name="AddCart"),
    path('reduce-cart/',OrderViews.ReduceCart,name="ReduceCart"),
    path('delete-product/',OrderViews.DeleteCartProduct,name="DeleteCartProduct"),
    path('change-shipping/',OrderViews.ChangeShipping,name="ChangeShipping"),

    path('view-wishlist/',OrderViews.ViewWishList,name="ViewWishList"),
    path('add-wishlist/',OrderViews.AddWishList,name="AddWishList"),
    path('reduce-wishlist/',OrderViews.ReduceWishList,name="ReduceWishList"),
]
