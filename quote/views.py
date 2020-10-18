from django.shortcuts import render
from .models import Quote
import random
# Create your views here.
def view_quote(request):
    obj = Quote.objects.all()
    obj = obj[random.randint(0, len(obj))]
    context = {
        'object': obj
    }
    return render(request, 'quote.html', context)