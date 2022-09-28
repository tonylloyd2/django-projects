from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from product.models import Product, ProductImage
from django.http import JsonResponse
from . import forms

UserModel = get_user_model()

def home(request):
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
        product['old_price'] = (product['product_price']*0.1)+product['product_price']

    return render(request,'home.html',{'products':products,'ProductImages':ProductImages})

def login(request):
    form = forms.LoginForm
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        return render(request,'auth/login.html',{'form':form})

    if request.method == 'POST':
        details = forms.LoginForm(request.POST)

        if details.is_valid():
            auth_login(request,authenticate(username = details.cleaned_data['email'],password = details.cleaned_data['password']))
            return redirect('home')
        elif not details.is_valid():
            return render(request,'auth/login.html',{'form':details})

        return render(request,'auth/login.html',{'form':form})

def logout(request):
    auth_logout(request)
    return redirect('home')

def register(request):
    form = forms.RegisterForm
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        return render(request,'auth/register.html',{'form':form})

    if request.method == 'POST':
        details = forms.RegisterForm(request.POST)

        if details.is_valid():
            return redirect('login')
        elif not details.is_valid():
            return render(request,'auth/register.html',{'form':details})

def AccountSettings(request):
    data = {}
    data['response'] = False
    if request.method == "GET":
        return render(request,'user/account-settings.html',data)
    
    elif request.method == "POST":
        proceed = True
        if authenticate(username = request.user.username,password = request.POST['current_password']):
            if len(request.POST['new_password']) >= 8:
                if request.POST['new_password'] == request.POST['confirm_password']:
                    user = UserModel.objects.get(username=request.user.username)
                    user.set_password(request.POST['new_password'])
                    user.save()
                    return JsonResponse({'success':'password updated succesfully'})

                elif request.POST['new_password'] != request.POST['confirm_password']:
                    return JsonResponse({'error':'Your passwords should match'})

            elif len(request.POST['new_password']) < 8:
                return JsonResponse({'error':'Your password should have atleast 8 characters'})

        else:
            return JsonResponse({'error':'The password you entered is wrong'})
        
            

