from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from shop.forms import OrderForm, CommentForm,  ProductModelForm
from shop.models import Product, Category, Order, Comment


# Create your views here.
def index(request,category_id = None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
       products = Product.objects.all()
    return render(request,'shop/home.html',{'products':products,'categories':categories})

def detail(request,id):
    product = Product.objects.get(id=id)
    comments = Comment.objects.filter(product_id=id)
    return render(request,'shop/detail.html',{'product':product,'comments':comments})





def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = OrderForm(request.GET)
        if form.is_valid():
            name = request.GET.get('name')
            phone_number = request.GET.get('phone_number')
            quantity = int(request.GET.get('quantity'))
            if product.quantity >= quantity:
                product.quantity -= quantity
                order = Order.objects.create(
                    name=name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=product
                )
                order.save()
                product.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order muvaffaqiyatli amalga oshirildi...'

                )

            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Nimadir hato...'
                )


    else:
        form = OrderForm()
    context = {
        'comments': Comment.objects.filter(product=product),
        'orders': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Comment
from .forms import CommentForm


def comment_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        form = CommentForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            commentary = Comment.objects.create(
                name=name,
                email=email,
                comment=comment,
                product=product
            )

            commentary.save()
            return redirect('comment_detail', pk=pk)
    else:
        form = CommentForm()
    context = {
        'comments': Comment.objects.filter(product=product),
        'form': form,
        'product': product,
    }
    return render(request, 'shop/detail.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductModelForm()

    context = {
        'form': form,
        'action': "Qo'shish",
    }
    return render(request, 'shop/add_product.html', context)


from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductModelForm  # Formani to'g'ri import qilganingizga ishonch hosil qiling
from .models import Product


def edit_product(request, pk):
    product = Product.objects.get(id=pk)  # Tahrir qilinadigan mahsulotni olish
    if request.method == "POST":
        # Formani POST so'rovi bilan, mahsulot instansiyasi bilan yaratish
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Mahsulotni tahrirlash va saqlash
            return redirect('home')  # Tahrirlangan mahsulot sahifasiga yo'naltirish
    else:
        # GET so'rovi uchun formani mahsulot bilan oldindan yaratish
        form = ProductModelForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'action': "O'zgartirish",  # Tahrirlash uchun action
    }
    return render(request, 'shop/add_product.html', context)


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('home')
    return render(request, 'shop/delete_product.html', {'product': product})