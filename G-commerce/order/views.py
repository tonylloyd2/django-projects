from django.shortcuts import render,redirect
from django.db.models import F
from cart.models import Cart
from order.models import Shipping

def checkout(request):
    if "HTTP_REFERER" in request.META:
        data = {}
        CartTotal = 0
        standard_shipping = list(Shipping.objects.filter(shipping_type='standard').values())[0]
        express_shipping = list(Shipping.objects.filter(shipping_type='express').values())[0]

        cart = list(Cart.objects.filter(user__user_id=request.user.user_id).values('no_items',cshipping=F('shipping__shipping_type'),cproduct_id=F('product__product_id'),cproduct_image=F('product__product_image'),cproduct_name=F('product__product_name'),cproduct_price=F('product__product_price')))
        shipping_fee = standard_shipping['shipping_fee']
        for item in cart:
            item['product_total'] = item['cproduct_price'] * item['no_items']
            if item['cshipping'] == 'express':
                shipping_fee = express_shipping['shipping_fee']

            CartTotal += item['product_total']

        CartTotal += shipping_fee
        data['cart'] = cart
        data['shipping_fee'] = shipping_fee
        data['CartTotal'] = CartTotal
        return render(request,'cart/checkout.html',data)
    elif "HTTP_REFERER" not in request.META:
        return redirect('ViewCart')