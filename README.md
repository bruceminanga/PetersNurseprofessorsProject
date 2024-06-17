Peters Project. 
This website uses the following systems:
1. Authentication System
2. Coupon System
3. 

To run this project locally, run:
python manage.py runserver --settings=peters_project.settings.local

To run it in production, namecheap for example, make sure that passenger_wsgi.py has the following content:
import os
import sys

from peters_project.wsgi import application #This will direct namecheap to my wsgi.py file


