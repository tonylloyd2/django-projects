from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, ProductImage
import ast

def SyncProductImage(request):
    products = list(Product.objects.all().values('product_id','product_image'))
    for product in products:
        try:
            productImage = ProductImage.objects.get(product__product_id=product['product_id'],image=product['product_image'])
        except ProductImage.DoesNotExist:
            productImage = ProductImage()
            productImage.product = Product.objects.get(product_id=product['product_id'])
            productImage.image = product['product_image']
            productImage.save()
    
    return JsonResponse({'s':'s'})

def ProductDetails(request,product_id,product_name):
    if request.method == "POST":
        pass
    data = {}
    product = list(Product.objects.filter(product_id=product_id).values())[0] 
    product['old_price'] = (product['product_price']*0.1)+product['product_price']
    product['product_info'] = ast.literal_eval(product['product_info'])
    related_products = list(Product.objects.filter(~Q(product_id=product_id),product_category__id=product['product_category_id']).order_by('product_id').values())
    related_images = list(ProductImage.objects.filter(~Q(product__product_id=product_id),product__product_category__id=product['product_category_id']).order_by('product_id').values())
    productImages = list(ProductImage.objects.filter(product_id=product_id).values())
    print(product['product_info'])

    for related_product in related_products:
        count = 1
        for related_image in related_images:
            if related_image['product_id'] == related_product['product_id']:
                related_image['index'] = count
                count+=1

                if count == 3:
                    break
        related_product['old_price'] = (related_product['product_price']*0.1)+related_product['product_price']

    data['product'] = product
    data['ProductImages'] = productImages
    data['related_products'] = related_products
    data['related_images'] = related_images
    data['product_id'] = product_id
    data['product_name'] = product_name
    return render(request,'product/product-details.html',data)

def shop(request):
    categories = list(Category.objects.all().values())
    products = list(Product.objects.all().values())
    ProductImages = list(ProductImage.objects.all().values())

    for category in categories:
        category['category_description'] = category['category_description'].split(',')

    for product in products:
        count = 1
        for image in ProductImages:
            if image['product_id'] == product['product_id']:
                image['index'] = count
                count+=1

                if count == 3:
                    break
        product['old_price'] = (product['product_price']*0.1)+product['product_price']
    
    data ={'products':products,'ProductImages':ProductImages,'categories':categories}

    return render(request,'product/shop.html',data)

def CategoryShop(request,category_id,category_name):
    products = list(Product.objects.filter(product_category__id=category_id).values())
    ProductImages = list(ProductImage.objects.filter(product__product_category__id=category_id).values())

    for product in products:
        count = 1
        for image in ProductImages:
            if image['product_id'] == product['product_id']:
                image['index'] = count
                count+=1

                if count == 3:
                    break
        product['old_price'] = (product['product_price']*0.1)+product['product_price']
    
    data ={'products':products,'ProductImages':ProductImages}

    return render(request,'product/category-shop.html',data)

def NewArrival(request):
    products = list(Product.objects.all().values())
    ProductImages = list(ProductImage.objects.all().values())

    for product in products:
        count = 1
        for image in ProductImages:
            if image['product_id'] == product['product_id']:
                image['index'] = count
                count+=1

                if count == 3:
                    break
    
    data ={'products':products,'ProductImages':ProductImages}
    return render(request,'product/new-arrival.html',data)

def FlashSale(request):
    products = list(Product.objects.all().values())
    ProductImages = list(ProductImage.objects.all().values())

    for product in products:
        count = 1
        for image in ProductImages:
            if image['product_id'] == product['product_id']:
                image['index'] = count
                count+=1

                if count == 3:
                    break
    
    data ={'products':products,'ProductImages':ProductImages}
    return render(request,'product/flash-sale.html',data)