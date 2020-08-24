from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from .models import *
from .utils import cookie_cart, cart_data
import json
from django.core.mail import send_mail, EmailMessage
from mysite.settings import EMAIL_HOST_USER
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

class IndexView(View):
    def get(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']
        a = SanPhamModel.objects.all()
        c = LoaiSPModel.objects.all()
        context = {
            'f': a,
            'danhmuc': c,
            'cart_items': cart_items,
        }
        return render(request, 'home/index.html', context)


def loaisp(request, id):
    data = cart_data(request)
    cart_items = data['cart_items']
    c = LoaiSPModel.objects.all()
    chitietsp = SanPhamModel.objects.all().filter(Loai_sp_id=id)
    return render(request, 'home/shop.html', {'f': chitietsp, 'danhmuc': c, 'cart_items': cart_items, })


def chitiet(request, id):
    data = cart_data(request)
    cart_items = data['cart_items']
    c = LoaiSPModel.objects.all()
    chitietsp = SanPhamModel.objects.all().filter(id=id)
    return render(request, 'home/product-single.html', {'f': chitietsp, 'danhmuc': c, 'cart_items': cart_items, })


def cart(request):
    c = LoaiSPModel.objects.all()
    data = cookie_cart(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'danhmuc': c
    }
    return render(request, 'home/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)
    return JsonResponse('Item was added', safe=False)


class Checkout(View):

    def get(self, request):
        c = LoaiSPModel.objects.all()
        data = cart_data(request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        context = {
            'items': items,
            'order': order,
            'cart_items': cart_items,
            'danhmuc': c
        }
        return render(request, 'home/checkout.html', context)

    def post(self, request):
        o = Order(request.POST)
        if o.is_valid():
            o.save()
            return HttpResponse('Lưu oke')
        else:
            return HttpResponse('Không lưu được')


def sendanemail(request):
    c = LoaiSPModel.objects.all()
    return render(request, "home/email_template.html", {'loaisp': c})


def SendPlainEmail(request):
    donhangtong = ('')
    sanpham = SanPhamModel.objects.all()
    for a in sanpham:
        ten = 'ten_' + str(a)
        mess_ten = request.POST.get(ten, '')
        gia = 'gia_' + str(a)
        mess_gia = request.POST.get(gia, '')
        soluong = 'soluong_' + str(a)
        mess_soluong = request.POST.get(soluong, '')

        donhang = (
                   '<strong>Tên Sản Phẩm:</strong>' + mess_ten + '<br>' +
                   '<strong>Giá Sản Phẩm:</strong>' + mess_gia + '<br>' +
                   '<strong>Số Lượng:</strong>' + mess_soluong+ '<br>' )
        donhangtong =(donhangtong+donhang)
    print(donhangtong)


    hoten = request.POST.get('hoten', '')
    diachi = request.POST.get('diachi', '')
    sdt = request.POST.get('sdt', '')
    thanhtien = request.POST.get('thanhtien', '')
    message = (''
               '<h1>XÁC NHẬN ĐƠN HÀNG</h1>' +
               '<strong>Họ Và Tên:</strong>' + hoten + '<br>' +
               '<strong>Địa Chỉ Nhận Hàng:</strong>' + diachi + '<br>' +
               '<strong>Số Điện Thoại Nhận Hàng:</strong>' + sdt + '<br>'+ '<h2>Đơn Hàng</h2>' +donhangtong+'<br>' +
               '<strong>Tổng Tiền:</strong>' + thanhtien + '<br>' +
               '<p>Cám ơn quý khách đã mua hàng tại Shop của chúng tôi, bộ phận giao hàng sẽ liên hệ với quý khách để xác nhận sau 5 phút kể từ khi đặt hàng thành công và chuyển hàng đến quý khách chậm nhất sau 24 tiếng.</p>')
    print('a', message)
    subject = ('Bạn đã đặt hàng từ shop thành công!!!')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'
    email.send()
    return HttpResponse("<h1>Cảm ơn bạn đã đặt hàng bên cửa hàng chúng tôi. Mời bạn kiểm tra email của mình để kiểm tra đơn hàng</h1>")
