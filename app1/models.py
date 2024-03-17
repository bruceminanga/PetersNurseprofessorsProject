from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)],
                   help_text='Percentage vaule (0 to 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code

class Customer(models.Model):  
    academic_level = models.CharField(max_length = 20, default=1)
    type_of_service = models.CharField(max_length = 30, default=1)   
    type_of_paper = models.CharField(max_length = 20, default=1)
    subject_area = models.CharField(max_length = 20, default=1)
    title = models.CharField(max_length = 20,)
    paper_instructions = models.CharField(max_length = 20,)
    additional_material = models.FileField(upload_to='images/%Y/%m/%d/', null=True, blank=True) 
    paper_format = models.CharField(max_length = 20,) 
    # number_of_pages = models.IntegerField()
    number_of_pages = models.CharField(max_length = 20, default=1)
    number_of_pages_increment = models.IntegerField(default=1)
    currency = models.CharField(max_length = 20,) 
    sources = models.IntegerField()
    powerpoint_slides = models.IntegerField() 
    deadline = models.CharField(max_length = 20,)
    writer_category = models.CharField(max_length = 20,)
    preferred_writers_id = models.IntegerField(null=True, blank=True)
    # additional_services = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    
class Product(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    slug = models.SlugField()
    description = models.TextField()
    

    def __str__(self):
        return self.name
    
    
# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )
    
class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def cost(self):
        return self.price * self.quantity
    
