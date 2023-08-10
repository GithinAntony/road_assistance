from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index/home.html')

def about(request):
    return render(request, 'index/about.html')

def service(request):
    return render(request, 'index/service.html')

def why(request):
    return render(request, 'index/why.html')

def contact_us(request):
    return render(request, 'index/contact.html')
