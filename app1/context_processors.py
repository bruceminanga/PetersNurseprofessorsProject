from .forms import NewsletterForm

def newsletter_form(request):
    return {'form3': NewsletterForm()}
