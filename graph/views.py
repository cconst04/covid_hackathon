from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from os.path import exists,join
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import csv
from django.db.models.functions import TruncHour,TruncMonth
from django.db.models import Count
import datetime
#templates/examples/dashboard/index.html
def index(request):
    return render(request,'index.html',{'data':list(Metric.objects.all())})
def upload_file(request):
    if request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        data.pop(0) #remove the description
        Metric.objects.all().delete()#delete previous records
        for row in data:
            postal_code_row = PostalCodeInfo.objects.filter(postal_code=row[2]).first()
            if not postal_code_row:#no such postal code exists continue
                continue
            record = Metric(ssn=row[0],reason=row[1],postal_code=postal_code_row,date=row[3])
            record.save()
        uploaded_file_url = fs.url(filename)
        return render(request,'index.html')
    return render(request,'upload.html')

def load_postal_codes(request):
    if request.method=='POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save("temp.csv", myfile)
        with open(join(settings.MEDIA_ROOT,"temp.csv"), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        data.pop(0)
        for row in data:
            if len(PostalCodeInfo.objects.filter(postal_code=row[0],lat=row[1],lon=row[2]))>0:
                continue
            record = PostalCodeInfo(postal_code=row[0],lat=row[1],lon=row[2])
            record.save()
        return HttpResponse("Success")

def per_hour_graph(request):
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()-datetime.timedelta(days=3)#show past 30 days
    delta = datetime.timedelta(days=1)
    # import pdb;pdb.set_trace()
    date_dict=[]
    while start_date >= end_date:
        start_hour = start_date.hour
        iter = 0
        while iter<=23:
            # import pdb;pdb.set_trace()

            date_obj = datetime.datetime(start_date.year,start_date.month,start_date.day,start_hour)
            date_obj-=datetime.timedelta(hours=iter)
            metric_rows = Metric.objects.filter(date__year=start_date.year,
                                              date__month=start_date.month,
                                              date__day=start_date.day,
                                              date__hour=date_obj.hour).order_by("-date")
            date_dict.append({'datetime':(date_obj+datetime.timedelta(hours=2)).strftime("%H:%M:%S %d-%m-%-Y"),'value':metric_rows.count()})
            iter+=1
        start_date -= delta
    print(date_dict)
    # result = Metric.objects.annotate(timestamp=TruncMonth('date')) \
    #                        .values('timestamp') \
    #                        .annotate(value=Count('id')) \
    #                        .values('timestamp', 'value')

    return JsonResponse({'data':date_dict})
