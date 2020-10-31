from django.shortcuts import render
from .models import Quote
import random
from django.contrib.auth import logout

# Create your views here.
def view_quote(request):
    user = request.user
    obj = Quote.objects.all()
    obj = obj[random.randint(0, len(obj))]
    context = {
        'object': obj,
        'user': user
    }
    return render(request, 'quote.html', context)