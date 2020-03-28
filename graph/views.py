from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from os.path import exists,join
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import csv
from django.db.models.functions import TruncHour,TruncMonth
from django.db.models import Count,F,Sum
from django.core.serializers import serialize
import datetime
#templates/examples/dashboard/index.html
def index(request):
    return render(request,'index.html')

def get_all_data(request):
    postal_list,count_per_city = today_count_by_region()
    return JsonResponse({
            'data':list(Metric.objects.all().values('reason','postal_code__postal_code','ssn','date','extras')),
            'count_per_hour':per_hour_graph(),
            'count_per_city_today':count_per_city,
            'count_per_postal':postal_list

        },safe=False)

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
            postal_code_row = PostalCodeInfo.objects.filter(postal_code=row[3]).first()
            if not postal_code_row:#no such postal code exists continue
                continue
            record = Metric(ssn=row[0],reason=row[1],postal_code=postal_code_row,date=row[2])
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

'''
Grouped by hour graph
'''
def per_hour_graph():
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()-datetime.timedelta(days=3)#show past 30 days
    delta = datetime.timedelta(days=1)
    date_dict=[]
    while start_date >= end_date:
        start_hour = start_date.hour
        iter = 0
        while iter<=23:
            date_obj = datetime.datetime(start_date.year,start_date.month,start_date.day,start_hour)
            date_obj-=datetime.timedelta(hours=iter)
            metric_rows = Metric.objects.filter(date__year=start_date.year,
                                              date__month=start_date.month,
                                              date__day=start_date.day,
                                              date__hour=date_obj.hour).order_by("-date")
            date_dict.append({'datetime':(date_obj).strftime("%Y-%m-%dT%H:%M:%SZ"),'value':metric_rows.count()})
            iter+=1
        start_date -= delta
    # print(date_dict)
    # result = Metric.objects.annotate(timestamp=TruncMonth('date')) \
    #                        .values('timestamp') \
    #                        .annotate(value=Count('id')) \
    #                        .values('timestamp', 'value')

    return date_dict
'''
Grouped by count graph
'''
def today_count_by_region():
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    cities_zip_code = {
        'Paphos':(8000,8500),
        'Nicosia':(1000,2500),
        'Larnaca':(6000,7200),
        'Limassol':(3000,4400)
    }
    result_list = [];
    count_per_city = []
    for city,postal_range in cities_zip_code.items():
        curr_city = Metric.objects.filter(date__range=(today_min, today_max),
                                          postal_code__postal_code__range=(postal_range[0],postal_range[1])) \
                                  .order_by("postal_code__postal_code")

        count_per_city.append({'name':city,'drilldown':city,'y':curr_city.count()})
        # result = Metric.objects.filter(date__range=(today_min, today_max),postal_code__postal_code__range=(range[0],range[1])) \
        #                        .values('postal_code__postal_code') \
        #                        .annotate(postal_code=F('postal_code__postal_code'),value=Count('id')) \
        #                        .values('postal_code','value')
        step_factor=20
        city_dict = {'name':city,'id':city,'data':[]}
        # import pdb;pdb.set_trace()
        for i in range(postal_range[0],postal_range[1],step_factor):
            result = curr_city.filter(date__range=(today_min, today_max),postal_code__postal_code__range=(i,i+20)) \
                                      .values('postal_code__postal_code') \
                                      .annotate(postal_code=F('postal_code__postal_code'),value=Count('id')) \
                                      .values('postal_code','value')
            if len(result)>0:
                city_dict['data'].append([str(i)+'-'+str(i+step_factor),result.aggregate(Sum('value'))['value__sum']])
        result_list.append(city_dict)
    print(count_per_city)
    return result_list,count_per_city
