from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.views import View
from shop.forms import OrderForm, CommentForm,  ProductModelForm
from shop.models import Product, Category, Order, Comment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductModelForm
from .models import Product
from django.urls import reverse

# Create your views here.
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q', '')
        filter = self.request.GET.get('filter', '')

        if category_id:
            if filter == 'expensive':
                queryset = queryset.filter(category_id=category_id).order_by('-price')[:5]
            elif filter == 'cheap':
                queryset = queryset.filter(category_id=category_id).order_by('price')[:5]
            elif filter == 'rating':
                queryset = queryset.filter(category_id=category_id, rating__gte=4).order_by('-rating')[:5]
            else:
                queryset = queryset.filter(category_id=category_id)
        else:
            if filter == 'expensive':
                queryset = queryset.order_by('-price')[:5]
            elif filter == 'cheap':
                queryset = queryset.order_by('price')[:5]
            elif filter == 'rating':
                queryset = queryset.filter(rating__gte=4).order_by('-rating')[:5]

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# Product detail methods

class DetailProductView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        context['comments'] = Comment.objects.filter(product=product,is_negative=False)
        context['positive'] = Comment.objects.filter(product=product, is_negative=False).count()
        context['related'] = Product.objects.filter(category_id=product.category).exclude(id=product.id)
        return context

# def detail(request,id):
#     product = Product.objects.get(id=id)
#     positive = Comment.objects.filter(product=product).count()
#     comments = Comment.objects.filter(product_id=id)
#     related = Product.objects.filter(category_id=product.category_id).exclude(id=product.id)
#     return render(request,'shop/detail.html',{'product':product,'comments':comments,'positive': positive,'related':related})
#

# Oder methods


class OrderCreateView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm()
        context = {
            'comments': Comment.objects.filter(product=product),
            'orders': form,
            'product': product,
        }
        return render(request, 'shop/detail.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
                print(f"Updated product quantity: {product.quantity}")  # Debug maqsadida
                order = form.save(commit=False)
                order.product = product
                order.save()
                messages.success(request, 'Buyurtma muvaffaqiyatli amalga oshirildi.')
            else:
                messages.error(request, 'Yetarli miqdorda mahsulot mavjud emas.')
        else:
            messages.error(request, 'Formada xatolik mavjud.')

        return redirect('order_detail', pk=pk)



# def order_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         form = OrderForm(request.GET)
#         if form.is_valid():
#             name = request.GET.get('name')
#             phone_number = request.GET.get('phone_number')
#             quantity = int(request.GET.get('quantity'))
#             if product.quantity >= quantity:
#                 product.quantity -= quantity
#                 order = Order.objects.create(
#                     name=name,
#                     phone_number=phone_number,
#                     quantity=quantity,
#                     product=product
#                 )
#                 order.save()
#                 product.save()
#                 messages.add_message(
#                     request,
#                     messages.SUCCESS,
#                     'Order muvaffaqiyatli amalga oshirildi...'
#
#                 )
#
#             else:
#                 messages.add_message(
#                     request,
#                     messages.ERROR,
#                     'Nimadir hato...'
#                 )
#
#
#     else:
#         form = OrderForm()
#     context = {
#         'comments': Comment.objects.filter(product=product),
#         'orders': form,
#         'product': product
#     }
#
#     return render(request, 'shop/detail.html', context)




# Comment methods

class CommentView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentForm()
        context = {
            'comments': Comment.objects.filter(product=product, is_negative=False),
            'form': form,
            'related': Product.objects.filter(category_id=product.category).exclude(id=product.id),
            'positive': Comment.objects.filter(product=product, is_negative=False).count(),
            'product': product,
        }
        return render(request, 'shop/detail.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            Comment.objects.create(
                name=name,
                email=email,
                comment=comment,
                product=product
            )
            return redirect('comment_detail', pk=pk)
        else:
            context = {
                'comments': Comment.objects.filter(product=product, is_negative=False),
                'form': form,
                'positive':Comment.objects.filter(product=product, is_negative=False).count(),
                'related': Product.objects.filter(category_id=product.category).exclude(id=product.id),
                'product': product,
            }
            return render(request, 'shop/detail.html', context)

# def comment_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         form = CommentForm(request.GET)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             comment = form.cleaned_data['comment']
#             commentary = Comment.objects.create(
#                 name=name,
#                 email=email,
#                 comment=comment,
#                 product=product
#             )
#
#             commentary.save()
#             return redirect('comment_detail', pk=pk)
#     else:
#         form = CommentForm()
#     context = {
#         'comments': Comment.objects.filter(product=product,is_negative=False),
#         'form': form,
#         'product': product,
#     }
#     return render(request, 'shop/detail.html', context)






# Create product methods

class CreateProductView(CreateView):
    model = Product
    template_name = 'shop/add_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('home')

# def add_product(request):
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ProductModelForm()
#
#     context = {
#         'form': form,
#         'action': "Qo'shish",
#     }
#     return render(request, 'shop/add_product.html', context)

# class CreateProductView(CreateView):
#     def post(self,request,*args,**kwargs):
#         form = ProductModelForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     def get(self,request,*args,**kwargs):
#         form = ProductModelForm()
#
#         context = {
#                  'form': form,
#                  'action': "Qo'shish",
#         }
#         return render(request, 'shop/add_product.html', context)






# Edit product

class UpdateProductView(UpdateView):
    model = Product
    template_name = 'shop/edit_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('home')
#
# class UpdateProductView(View):
#     def get(self, request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         form = ProductModelForm(instance=product)
#         context = {
#             'form': form,
#             'product': product,
#             'action': "O'zgartirish",
#         }
#         return render(request, 'shop/edit_product.html', context)
#
#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         form = ProductModelForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
# def edit_product(request, pk):
#     product = Product.objects.get(id=pk)
#     if request.method == "POST":
#
#         form = ProductModelForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ProductModelForm(instance=product)
#
#     context = {
#         'form': form,
#         'product': product,
#         'action': "O'zgartirish",
#     }
#     return render(request, 'shop/edit_product.html', context)






# Delete product methods

class DeleteProductView(DeleteView):
    model = Product
    template_name = 'shop/delete_product.html'
    success_url = reverse_lazy('home')


# class DeleteProductView(View):
#      def post(self, request, pk):
#          product = get_object_or_404(Product, pk=pk)
#          product.delete()
#          return redirect('home')
#
#      def get(self, request, pk):
#          product = get_object_or_404(Product, pk=pk)
#          return render(request, 'shop/delete_product.html', {'product': product})



# def delete_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         product.delete()
#         return redirect('home')
#     return render(request, 'shop/delete_product.html', {'product': product})

