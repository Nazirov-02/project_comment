from django.db import models
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    title = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,related_name='product')
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=14)
    discount = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices,default=RatingChoice.ONE)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='media/products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'products'

    def discount_price(self):
        if self.discount > 0:
            self.price = self.price * Decimal((1 - self.discount / 100))
        return self.price.quantize(Decimal('0.01'))

    def img_url(self):
        return self.image.url

class Order(BaseModel):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(region="UZ")
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,related_name='order')

    def __str__(self):
        return f'{self.name}, {self.phone_number}'

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,related_name='comment')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.name}, {self.email}, {self.product.name}'
