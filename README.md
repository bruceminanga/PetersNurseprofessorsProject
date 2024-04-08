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
# sys.path.insert(0, os.path.dirname(__file__))


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python %s\n' % sys.version.split()[0]
#     response = '\n'.join([message, version])
#     return [response.encode()]

from peters_project.wsgi import application #This will direct namecheap to my wsgi.py file


