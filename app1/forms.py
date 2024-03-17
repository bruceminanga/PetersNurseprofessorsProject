# import the standard Django Forms
from django import forms
from app1.models import Customer

class CouponApplyForm(forms.Form):
    code = forms.CharField()

    

class NewCustomerForm(forms.ModelForm):
    ACADEMIC_LEVEL_CHOICES = [
    ("Highschool", "Highschool"),
    ("Undergraduate", "Undergraduate"),
    ("Masters", "Masters"),
    ("Doctoral", "Doctoral"),
    ("TEAS 7", "TEAS 7"),
    ("HESI", "HESI"),
    ]

    TYPE_OF_SERVICE_CHOICES = [
        ("Writing from scratch", "Writing from scratch"),
        ("Editing", "Editing"),
        ("Problem solving", "Problem solving"),
        ("Paraphrasing/Rewriting", "Paraphrasing/Rewriting"),
        ("TEAS 7", "TEAS 7"),
        ("HESI", "HESI"),
    ]

    TYPE_OF_PAPER_CHOICES = [
        ("Essay", "Essay"),
        ("Article", "Article"),
        ("Assignment", "Assignment"),
        ("Content", "Content"),
        ("Business plan", "Business plan"),
        ("Movie Review", "Movie Review"),
    ]

    SUBJECT_AREA_CHOICES = [
        ('Any', 'Select Subject'),
        ('Archaeology', 'Archaeology'),
        ('Architecture', 'Architecture'),
        ('Arts', 'Arts'),
        ('Astronomy', 'Astronomy'),
        ('Biology', 'Biology'),
        ('Business', 'Business'),
        ('Chemistry', 'Chemistry'),
        ('Childcare', 'Childcare'),
        ('Computers', 'Computers'),
        ('Counseling', 'Counseling'),
        ('Criminology', 'Criminology'),
        ('Economics', 'Economics'),
        ('Education', 'Education'),
        ('Engineering', 'Engineering'),
        ('Environmental-Studies', 'Environmental-Studies'),
        ('Ethics', 'Ethics'),
        ('Ethnic-Studies', 'Ethnic-Studies'),
        ('Finance', 'Finance'),
        ('Food-Nutrition', 'Food-Nutrition'),
        ('Geography', 'Geography'),
        ('Healthcare', 'Healthcare'),
        ('HESI Test', 'HESI Test'),
        ('History', 'History'),
        ('Law', 'Law'),
        ('Linguistics', 'Linguistics'),
        ('Literature', 'Literature'),
        ('Management', 'Management'),
        ('Mathematics', 'Mathematics'),
        ('Medicine', 'Medicine'),
        ('Music', 'Music'),
        ('NACE', 'NACE'),
        ('NCLEX-RN', 'NCLEX-RN'),
        ('Nursing', 'Nursing'),
        ('Philosophy', 'Philosophy'),
        ('Physical-Education', 'Physical-Education'),
        ('Physics', 'Physics'),
        ('Political-Science', 'Political-Science'),
        ('Programming', 'Programming'),
        ('Psychology', 'Psychology'),
        ('Religion', 'Religion'),
        ('Sociology', 'Sociology'),
        ('Statistics', 'Statistics'),
        ('TEAS 7 Test', 'TEAS 7 Test'),
    ]

    NUMBER_OF_PAGES_CHOICES = [
        ('Double Spaced', 'Double Spaced'),
        ('Single Spaced', 'Single Spaced'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ]

    DEADLINE_CHOICES = [
        ('6hrs', '6hrs'),
        ('12hrs', '12hrs'),
        ('24hrs', '24hrs'),
        ('48hrs', '48hrs'),
        ('5days', '5days'),
        ('10days', '10days'),
        ('14days', '14days'),
        ('30days', '30days'),
    ]

    WRITER_CATEGORY_CHOICES = [
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
        ('Platinum', 'Platinum'),
    ]

    PAPER_FORMAT = [
        ('APA', 'APA'),
        ('MLA', 'MLA'),
        ('HAVARD', 'HAVARD'),
        ('CHICAGO', 'CHICAGO'),
        ('TURABIAN', 'TURABIAN'),
        ('OTHER', 'OTHER'),
    ]



    academic_level = forms.ChoiceField(choices=ACADEMIC_LEVEL_CHOICES)
    type_of_service = forms.ChoiceField(choices=TYPE_OF_SERVICE_CHOICES)   
    type_of_paper = forms.ChoiceField(choices=TYPE_OF_PAPER_CHOICES)
    subject_area = forms.ChoiceField(choices=SUBJECT_AREA_CHOICES)
    title = forms.CharField(widget = forms.PasswordInput())
    paper_instructions = forms.CharField(widget=forms.Textarea, max_length=200, required=False)
    additional_material = forms.FileField(required=False)  
    paper_format = forms.ChoiceField(choices=PAPER_FORMAT) 
    number_of_pages = forms.ChoiceField(choices=NUMBER_OF_PAGES_CHOICES)
    number_of_pages_increment = forms.IntegerField(min_value=1, max_value=10, initial=1)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    sources = forms.IntegerField(min_value=1, max_value=10, initial=1)
    powerpoint_slides = forms.IntegerField(min_value=0, max_value=10, initial=0)
    deadline = forms.ChoiceField(choices=DEADLINE_CHOICES)
    writer_category = forms.ChoiceField(choices=WRITER_CATEGORY_CHOICES)
    preferred_writers_id = forms.IntegerField(required=False)
    # additional_services = forms.IntegerField()
    
    class Meta:
        model = Customer
        fields = ['academic_level', 'type_of_service', 'type_of_paper', 'subject_area', 'title','paper_instructions','additional_material', 'paper_format', 'number_of_pages', 'currency', 'sources','powerpoint_slides', 'deadline', 'writer_category', 'preferred_writers_id']