from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from shop.forms import OrderForm, CommentForm,  ProductModelForm
from shop.models import Product, Category, Order, Comment


# Create your views here.
def index(request,category_id = None):
    search_query = request.GET.get('q','')
    filter = request.GET.get('filter','')
    categories = Category.objects.all()
    if category_id:
        if filter == 'expensive':
            products = Product.objects.filter(category_id=category_id).order_by('-price')[:5]
        elif filter == 'cheap':
            products = Product.objects.filter(category_id=category_id).order_by('price')[:5]
        elif filter == 'rating':
            products = Product.objects.filter(category_id=category_id,rating__gte=4).order_by('-rating')[:5]
        else:
            products = Product.objects.filter(category_id=category_id)
    else:
        if filter == 'expensive':
            products = Product.objects.all().order_by('-price')[:5]
        elif filter == 'cheap':
            products = Product.objects.all().order_by('price')[:5]
        elif filter == 'rating':
            products = Product.objects.filter(rating__gte=4).order_by('-rating')[:5]
        else:
            products = Product.objects.all()
    if search_query:
        products = Product.objects.filter(name__icontains=search_query,category_id=category_id)
    return render(request,'shop/home.html',{'products':products,'categories':categories})

def detail(request,id):
    product = Product.objects.get(id=id)
    positive = Comment.objects.filter(product=product, is_negative=False).count()
    comments = Comment.objects.filter(product_id=id)
    related = Product.objects.filter(category_id=product.category_id).exclude(id=product.id)
    return render(request,'shop/detail.html',{'product':product,'comments':comments,'positive': positive,'related':related})





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
        'comments': Comment.objects.filter(product=product,is_negative=False),
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
from .forms import ProductModelForm
from .models import Product


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":

        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductModelForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'action': "O'zgartirish",
    }
    return render(request, 'shop/edit_product.html', context)


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('home')
    return render(request, 'shop/delete_product.html', {'product': product})

