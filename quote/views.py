from django.shortcuts import render
from .models import Quote
import random
from django.contrib.auth import logout
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Quote

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

class QuoteDelete(DeleteView):
    model = Quote
    success_url = reverse_lazy('view_my_quotes')