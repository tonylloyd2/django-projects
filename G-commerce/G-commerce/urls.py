from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from user import views as UserViews
from product.views import SyncProductImage

urlpatterns = [
    path('sync-product-image/',SyncProductImage,name="SyncProductImage"),
    path('admin/', admin.site.urls),
    path('',UserViews.home,name="home"),
    path('user/',include('user.urls')),
    path('auth/',include('user.urls')),
    path('product/',include('product.urls')),
    path('cart/',include('cart.urls')),
    path('order/',include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()
