from django.urls import path
from . import views as OrderViews

urlpatterns = [
    path('checkout',OrderViews.checkout,name="checkout"),
]
