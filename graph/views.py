from django.http import HttpResponse
from django.shortcuts import render
#templates/examples/dashboard/index.html
def index(request):
    return render(request,'examples/dashboard/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")
