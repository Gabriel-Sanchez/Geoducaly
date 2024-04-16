from django.shortcuts import render

# Create your views here.

def calendario(request):
    return render(request,'calendarioapp/calendario.html')


from django.shortcuts import render
from schedule.models import Calendar

def calendar_view(request):
    calendar = Calendar.objects.get(name='Mi calendario')
    return render(request, 'calendarioapp/calendario.html', {'calendar': calendar})
