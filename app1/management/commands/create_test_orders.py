from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app1.models import Order
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates test orders for bidding'

    def handle(self, *args, **kwargs):
        # Ensure there's at least one user
        user, created = User.objects.get_or_create(username='testuser')
        
        paper_types = ['Essay', 'Research Paper', 'Thesis', 'Dissertation']
        subjects = ['History', 'Science', 'Literature', 'Philosophy']
        
        for i in range(10):  # Create 10 test orders
            order = Order.objects.create(
                writer=user,
                title=f'Test Order {i+1}',
                type_of_paper=random.choice(paper_types),
                subject_area=random.choice(subjects),
                academic_level='Undergraduate',
                number_of_pages=random.randint(2, 10),
                deadline=timezone.now() + timezone.timedelta(days=random.randint(1, 14)),
                price=random.uniform(50.0, 200.0),
                status='unpaid',
                bidding=True,
                words=random.randint(500, 2500)
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created order {order.id}'))