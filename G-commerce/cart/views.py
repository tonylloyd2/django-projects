from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import F
from cart.models import Cart, WishList
from product.models import Product
from django.contrib.auth import get_user_model
from order.models import Shipping

UserModel = get_user_model()


def global_cart(request):
    data = {}
    data['shipping_fee'] = 0
    data['grand_total'] = 0
    if request.user.is_authenticated:
        standard_shipping = list(Shipping.objects.filter(shipping_type='standard').values())[0]
        express_shipping = list(Shipping.objects.filter(shipping_type='express').values())[0]
        cart = list(Cart.objects.filter(user__user_id=request.user.user_id).values('no_items',Gproduct_name=F('product__product_name'),Gproduct_id=F('product__product_id'),Gproduct_price=F('product__product_price'),Gproduct_image=F('product__product_image'),Gshipping=F('shipping__shipping_type')))
        
        grand_total = 0
        shipping_fee = standard_shipping['shipping_fee']

        count = 0

        for item in cart:
            count += 1
            grand_total += item['Gproduct_price']
            if item['Gshipping'] == 'express':
                shipping_fee = express_shipping['shipping_fee']

            item['item_qty'] = "{:02d}".format(item['no_items'])

        if len(cart) == 0:
            shipping_fee = 0

        grand_total += shipping_fee

        data['cart'] = cart
        data['shipping_fee'] = shipping_fee
        data['grand_total'] = grand_total
        data['Gcount'] = "{:02d}".format(count)
        
    return {'GlobalCart':data}

def NewCartTotal(user_id):
    data = {}
    cart = list(Cart.objects.filter(user__user_id=user_id).values('no_items',cproduct_price=F('product__product_price')))
    CartTotal = 0
    for item in cart:
        item['ctotal_price'] =  item['cproduct_price'] * item['no_items']
        CartTotal+=item['ctotal_price']

    return CartTotal

def AddCart(request):
    try:
        cart = Cart.objects.get(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        cart = Cart.objects.filter(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        cart.update(no_items=F('no_items')+1)
        recart = list(cart.values('no_items',price=F('product__product_price')))[0]
        return JsonResponse({'no_items':recart['no_items'],'sub_total':(recart['price']*recart['no_items']),'cart_total':NewCartTotal(request.user.user_id)})

    except Cart.DoesNotExist:
        cart = Cart()
        cart.user = UserModel.objects.get(user_id=request.user.user_id)
        cart.product = Product.objects.get(product_id=request.POST['product_id'])
        cart.no_items = request.POST['no_items']
        cart.save()
        return JsonResponse({'success':'success'})

def ReduceCart(request):
    try:
        cart = Cart.objects.get(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        cart = Cart.objects.filter(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        cart.update(no_items=F('no_items')-1)
        recart = list(cart.values('no_items',price=F('product__product_price')))[0]
        return JsonResponse({'no_items':recart['no_items'],'sub_total':(recart['price']*recart['no_items']),'cart_total':NewCartTotal(request.user.user_id)})

    except Cart.DoesNotExist:
        cart = Cart()
        cart.user = UserModel.objects.get(user_id=request.user.user_id)
        cart.product = Product.objects.get(product_id=request.POST['product_id'])
        cart.no_items = int(request.POST['no_items'])
        cart.save()
        return JsonResponse({'success':'success'})


def ViewCart(request):
    data = {}
    shipping = list(Shipping.objects.all().values())
    data['CartIsEmpty'] = False
    cart = list(Cart.objects.filter(user__user_id=request.user.user_id).values('no_items',cshipping=F('shipping__shipping_type'),cproduct_id=F('product__product_id'),cproduct_image=F('product__product_image'),cproduct_name=F('product__product_name'),cproduct_price=F('product__product_price')))
    if len(cart) == 0:
        data['CartIsEmpty'] = True
        for cshipping in shipping:
            cshipping['shipping_fee'] = 0

    CartTotal = 0
    cshipping = 'standard'
    for item in cart:
        item['ctotal_price'] =  item['cproduct_price'] * item['no_items']
        CartTotal+=item['ctotal_price']
        if item['cshipping']=='express':
            cshipping = 'express'

    data['CartTotal'] = CartTotal
    data['cart'] = cart
    data['shipping'] = shipping
    data['cshipping'] = cshipping
    return render(request,'cart/view-cart.html',data)

def DeleteCartProduct(request):
    try:
        product = Cart.objects.filter(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        product.delete()
        return JsonResponse({'success':'success'})

    except Cart.DoesNotExist:
        return JsonResponse({'success':'success'})

def ChangeShipping(request):
    shipping = Shipping.objects.get(shipping_type=request.POST['shipping'])
    cart = Cart.objects.filter(user__user_id=request.user.user_id)
    cart.update(shipping=shipping)
    return JsonResponse({'success':'success'})


def AddWishList(request):
    try:
        wishlist = WishList.objects.get(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        wishlist = WishList.objects.filter(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        wishlist.update(no_items=F('no_items')+1)
        rewishlist = list(wishlist.values('no_items',price=F('product__product_price')))[0]
        return JsonResponse({'no_items':rewishlist['no_items'],'sub_total':(rewishlist['price']*rewishlist['no_items'])})

    except WishList.DoesNotExist:
        wishlist = WishList()
        wishlist.user = UserModel.objects.get(user_id=request.user.user_id)
        wishlist.product = Product.objects.get(product_id=request.POST['product_id'])
        wishlist.no_items = request.POST['no_items']
        wishlist.save()
        return JsonResponse({'success':'success'})

def ReduceWishList(request):
    try:
        wishlist = WishList.objects.get(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        wishlist = WishList.objects.filter(user__user_id=request.user.user_id,product__product_id=request.POST['product_id'])
        wishlist.update(no_items=F('no_items')-1)
        rewishlist = list(wishlist.values('no_items',price=F('product__product_price')))[0]
        return JsonResponse({'no_items':rewishlist['no_items'],'sub_total':(rewishlist['price']*rewishlist['no_items'])})

    except WishList.DoesNotExist:
        return JsonResponse({'success':'success'})

def ViewWishList(request):
    data = {}
    wishlist = list(WishList.objects.filter(user__user_id=request.user.user_id).values('no_items',wproduct_id=F('product__product_id'),wproduct_image=F('product__product_image'),wproduct_name=F('product__product_name'),wproduct_price=F('product__product_price'),sub_total=F('no_items')*F('product__product_price')))
    
    data['wishlist'] = wishlist
    return render(request,'cart/wishlist.html',data)

