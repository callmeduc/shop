from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class LoaiSPModel(models.Model):
    Ma_loai = models.CharField(max_length=10, verbose_name='Mã Loại Sản Phẩn', blank=True, )
    Loai_sp = models.CharField(max_length=50, verbose_name='Tên Loại Sản Phẩn', blank=True, )
    Mo_ta = models.TextField(verbose_name='Mô Tả')

    def __str__(self):
        return self.Loai_sp


class SanPhamModel(models.Model):
    Loai_sp = models.ForeignKey(LoaiSPModel, on_delete=models.CASCADE, default=1, verbose_name='Loại Sản Phẩm')
    Ma_sp = models.CharField(max_length=10, verbose_name='Mã Sản Phẩm')
    Ten_sp = models.CharField(max_length=50, verbose_name='Tên Sản Phẩm', blank=True)
    Mo_ta = models.TextField(verbose_name='Mô Tả')
    Gia_nhap = models.IntegerField(verbose_name='Giá Nhập', blank=True, default=0)
    Sale = models.PositiveIntegerField(blank=True, default=0)
    Gia_ban = models.IntegerField(verbose_name='Giá Bán', blank=True, default=200000)
    Gia_sale = models.IntegerField(verbose_name='Giá Sale', default=150000)
    Hang_ton = models.IntegerField(verbose_name='Hàng Tồn', default=100)
    Anh = models.ImageField(upload_to='images')

    def __str__(self):
        return self.Ten_sp

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f" {self.customer.name} - {self.id} - {self.complete}"

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            if not order_item.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        # show những items đã order
        total = sum(item.get_total for item in order_items)
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum(item.quantity for item in order_items)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(SanPhamModel, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.Ten_sp

    @property
    def get_total(self):
        total = self.product.Gia_sale * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    hoten = models.CharField(max_length=200, null=False)
    diachi = models.CharField(max_length=200, null=False)
    sdt = models.CharField(max_length=200, null=False)
    Email = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
