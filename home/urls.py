from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('index/', views.IndexView.as_view(), name='index'),
                  path('index/chitiet/<int:id>/', views.chitiet, name='chitiet'),
                  path('index/danhmuc/<int:id>/', views.loaisp, ),
                  path('cart/', views.cart, name='cart'),
                  path('update_item/', views.updateItem, name="update_item"),
                  path('checkout/', views.Checkout.as_view(), name="checkout"),
                  path('sendmail/', views.sendanemail, name='sendmail'),
                  path('send_plain_mail', views.SendPlainEmail, name='plain_email'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
