from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Discount, Coupon, Order, Product, Message, Referral, Wallet, Transaction, LineItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DiscountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'user', 'code', 'description', 'amount', 'expiry_date']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'valid_from', 'valid_to', 'discount', 'active']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'academic_level', 'type_of_service', 'type_of_paper', 'subject_area',
            'title', 'paper_instructions', 'additional_material', 'paper_format',
            'number_of_pages', 'number_of_pages_increment', 'currency', 'sources',
            'powerpoint_slides', 'deadline', 'writer_category', 'preferred_writers_id',
            'price', 'writer', 'words', 'amount_due', 'name', 'email', 'postal_code',
            'address', 'date', 'paid', 'bidding', 'status', 'total_cost'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'slug', 'description']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'user', 'sender', 'subject', 'body', 'date_sent', 'is_read', 'receiver',
            'content', 'sent_at', 'read', 'status'
        ]

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred', 'amount_earned', 'date', 'name']

class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'date', 'description', 'amount', 'balance_after']

class LineItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = LineItem
        fields = ['id', 'order', 'product', 'price', 'quantity', 'date_added', 'cost']
