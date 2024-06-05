from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # Discount amount in percentage
    expiry_date = models.DateField()


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True, blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)],
                   help_text='Percentage vaule (0 to 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code

from django.db import models

from django.db import models

class Order(models.Model):
    academic_level = models.CharField(max_length=20, default='1')
    type_of_service = models.CharField(max_length=30, default='1')
    type_of_paper = models.CharField(max_length=255, default='Unknown')
    subject_area = models.CharField(max_length=20, default='1')
    title = models.CharField(max_length=255, default='Untitled')
    paper_instructions = models.TextField(default='')
    additional_material = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    paper_format = models.CharField(max_length=20, default='Unknown')
    number_of_pages = models.CharField(max_length=20, default='1')
    number_of_pages_increment = models.IntegerField(default=1)
    currency = models.CharField(max_length=20, default='USD')
    sources = models.IntegerField(default=0)
    powerpoint_slides = models.IntegerField(default=0)
    deadline = models.CharField(max_length=20, default='None')
    writer_category = models.CharField(max_length=20, default='Standard')
    preferred_writers_id = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('approved', 'Approved'),
        ('revision', 'Revision'),
        ('editing', 'Editing')
    ]

    writer = models.CharField(max_length=255, default='Untitled')
    words = models.IntegerField(default=0)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField(default=0)
    address = models.CharField(max_length=191, default='Unknown')
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    bidding = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([li.cost() for li in self.lineitem_set.all()])

    
class Product(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    slug = models.SlugField()
    description = models.TextField()
    

    def __str__(self):
        return self.name
    
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Ensure user with ID 1 exists
    sender = models.CharField(max_length=191)
    subject = models.CharField(max_length=255, default='No Subject')
    body = models.TextField(default='No Content')
    date_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    receiver = models.CharField(max_length=191)
    content = models.TextField(default='No Content')  # Add a default value for content
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return "{} -> {}: {}".format(self.sender, self.subject, self.receiver)

    @property
    def status(self):
        return 'Read' if self.is_read else 'Unread'

class Referral(models.Model):
    referrer = models.CharField(max_length=191)
    referred = models.CharField(max_length=191)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, default='empty') 

    def __str__(self):
        return "{} referred {}: ${}".format(self.referrer, self.referred, self.amount_earned)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "{}: ${}".format(self.user.username, self.balance)
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
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
    
