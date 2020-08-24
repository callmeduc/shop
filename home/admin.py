from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer,CustomerAdmin)


class LoaiSPModelAdmin(admin.ModelAdmin):
    list_display = ('id','Loai_sp',)
admin.site.register(LoaiSPModel, LoaiSPModelAdmin)


class SanPhamModelAdmin(admin.ModelAdmin):
    list_display = ('Ma_sp','Ten_sp','Loai_sp')
admin.site.register(SanPhamModel, SanPhamModelAdmin)


class OrderAdmin(admin.ModelAdmin):
   list_display = ('id','customer',)
admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderItem, OrderItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(ShippingAddress, ShippingAddressAdmin)