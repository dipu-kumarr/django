from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def calculator():
    x=1
    y=2
    return x

def say_hello(request):
    x=calculator()
    return render(request,'hello.html',{'name':'dipu '})