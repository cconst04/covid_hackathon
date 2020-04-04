from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from os.path import exists,join
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import csv
from django.db.models.functions import TruncHour,TruncMonth,TruncDay
from django.db.models import Count,F,Sum,Avg
from django.core.serializers import serialize
import datetime
from django.utils import timezone
import os

#templates/examples/dashboard/index.html
def index(request):
    try:
        curr_date = datetime.datetime.strptime(request.GET['date'],"%Y-%m-%d")
    except:
        curr_date = datetime.datetime.now()
    # import pdb;pdb.set_trace()
    return render(request,'index.html',sidebar_stats(curr_date))

def get_all_data(request):
    try:
        curr_date = datetime.datetime.strptime(request.GET['date'],"%Y-%m-%d")
    except:
        curr_date = datetime.datetime.now()
    postal_list,count_per_city = today_count_by_region(curr_date)
    baseline_comparison,daily_count_per_city = hourly_baseline_comparison(curr_date)
    return JsonResponse({
            'data':list(Metric.objects.all().values('reason','postal_code__postal_code','ssn','date','extras')),
            'count_per_hour':per_hour_graph(curr_date),
            'count_per_city_today':count_per_city,
            'count_per_postal':postal_list,
            'count_per_coordinate':count_per_coordinate(curr_date),
            'category_per_city':category_per_city(curr_date),
            'baseline_comparison':baseline_comparison,
            'daily_count_per_city':daily_count_per_city,
            'fines':list(Fine.objects.all().values('date','lat','lon','count'))

        },safe=False)

def history_page(request):
    return render(request,'history.html')


def upload_fines(request):
    if request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME)):
            os.remove(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME))
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        data.pop(0) #remove the description
        # Fine.objects.all().delete()#delete previous records
        for row in data:
            record = Fine(date=row[0],lat=row[1],lon=row[2],count=row[3])
            record.save()
        uploaded_file_url = fs.url(filename)
        # return render(request,'upload.html')
    return render(request,'upload.html')

def upload_file(request):
    if request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME)):
            os.remove(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME))
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        data.pop(0) #remove the description
        # Metric.objects.all().delete()#delete previous records
        for row in data:
            postal_code_row = PostalCodeInfo.objects.filter(postal_code=row[3]).first()
            person_row = Person.objects.filter(ssn=row[0]).first()
            if not person_row:#no such person exists
                continue
            if not postal_code_row:#no such postal code exists continue
                continue
            record = Metric(ssn=person_row,reason=row[1],postal_code=postal_code_row,date=row[2])
            record.save()
        uploaded_file_url = fs.url(filename)
        # return render(request,'upload.html')
    return render(request,'upload.html')

def load_postal_codes(request):
    if request.method=='POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME)):
            os.remove(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME))
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
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
def per_hour_graph(curr_date):
    start_date = curr_date
    end_date = curr_date-datetime.timedelta(days=1)#show past 30 days
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
def today_count_by_region(curr_date):
    today_min = datetime.datetime.combine(curr_date, datetime.time.min)
    today_max = datetime.datetime.combine(today_min, datetime.time.max)


    result_list = []
    count_per_city = []
    for city,postal_range in settings.CITIES_ZIP_CODE.items():
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

def count_per_coordinate(curr_date):
    today_min = datetime.datetime.combine(curr_date, datetime.time.min)
    today_max = datetime.datetime.combine(today_min, datetime.time.max)
    result = Metric.objects.filter(date__range=(today_min, today_max)) \
                           .values('postal_code__lat','postal_code__lon') \
                           .annotate(lat=F('postal_code__lat'),lon=F('postal_code__lon'),value=Count('id')) \
                           .values('lat','lon','value')
    return list(result)

def category_per_city(curr_date):
    today_min = datetime.datetime.combine(curr_date, datetime.time.min)
    today_max = datetime.datetime.combine(today_min, datetime.time.max)
    data = []
    for city in settings.CITIES_ZIP_CODE:
        code_from = settings.CITIES_ZIP_CODE[city][0]
        code_to = settings.CITIES_ZIP_CODE[city][1]
        result = Metric.objects.filter(date__range=(today_min, today_max),
                                       postal_code__postal_code__range=(code_from,code_to)) \
                               .values('reason') \
                               .annotate(value=Count('id')) \
                               .values('reason','value') \
                               .order_by('reason')
        city_stats = [city] + [0]*8
        sum = 0
        for item in result:
            sum+=item['value']
            city_stats[item['reason']]=item['value']

        city_stats.append(sum)
        city_stats.append(-1)
        data.append(city_stats)
    return data


def hourly_baseline_comparison(curr_date):
    today_min = datetime.datetime.combine(curr_date, datetime.time.min)
    today_max = datetime.datetime.combine(today_min, datetime.time.max)
    yesterday = curr_date-datetime.timedelta(days=1)
    daily_count = {}
    avg = [0]*24
    date_now = timezone.now()
    oldest_day = (date_now-Metric.objects.all().order_by('date').first().date).days
    for i in range(1,oldest_day+1):
        curr_day = curr_date-datetime.timedelta(days=i)
        for city in settings.CITIES_ZIP_CODE:#count for each city daily count
            code_from = settings.CITIES_ZIP_CODE[city][0]
            code_to = settings.CITIES_ZIP_CODE[city][1]
            result = Metric.objects.filter(date__day=curr_day.day,
                                           date__month=curr_day.month,
                                           date__year=curr_day.year,
                                           postal_code__postal_code__range=(code_from,code_to))
            if not city in daily_count:
                daily_count[city]=[{'date':curr_day,'value':len(result)}]
            else:
                daily_count[city].append({'date':curr_day,'value':len(result)})

        result = Metric.objects.filter(date__day=curr_day.day,
                                       date__month=curr_day.month,
                                       date__year=curr_day.year) \
                               .annotate(hour=TruncHour('date')) \
                               .values('hour') \
                               .annotate(hour_count=Count('hour')) \
                               .values('hour','hour_count')
        for item in result:
            # import pdb;pdb.set_trace()
            avg[item['hour'].hour]+=item['hour_count']
    avg = [item/(oldest_day) for item in avg]


    today_records = Metric.objects.filter(date__range=(today_min, today_max)) \
                                  .annotate(hour=TruncHour('date')) \
                                  .values('hour') \
                                  .annotate(hour_count=Count('hour')) \
                                  .values('hour','hour_count')
    # import pdb;pdb.set_trace()
    result_list = [0]*24
    for i in range(len(today_records)):
        temp = {
        'date':today_records[i]['hour'].strftime("%Y-%m-%dT%H:%M:%SZ"),
        'value1':today_records[i]['hour_count'],
        'value2':avg[today_records[i]['hour'].hour],
        'previousDate':today_records[i]['hour'].strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        result_list[today_records[i]['hour'].hour]=temp
    print(daily_count)
    return result_list,daily_count

def load_id_age(request):
    if request.method=='POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME)):
            os.remove(os.path.join(settings.MEDIA_ROOT, settings.CSV_FILENAME))
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        data.pop(0)
        for row in data:
            if len(Person.objects.filter(ssn=row[0],age=row[1]))>0:
                continue
            record = Person(ssn=row[0],age=row[1])
            record.save()
        return HttpResponse("Success")


def sidebar_stats(curr_date):
    today_min = datetime.datetime.combine(curr_date, datetime.time.min)
    today_max = datetime.datetime.combine(today_min, datetime.time.max)
    yesterday_min = today_min - datetime.timedelta(days=1)
    yesterday_max = today_max - datetime.timedelta(days=1)
    ranges = [(10,20),(21,40),(41,60),(61,100)]
    pct_per_age = []
    pct_change = []
    for item in ranges:
        result = Metric.objects.filter(ssn__age__range=(item[0],item[1]),
                                       date__range=(today_min,today_max)) \
                               .distinct('ssn__ssn')
        total = Metric.objects.filter(ssn__age__range=(item[0],item[1])).distinct('ssn')
        pct_today = 100*len(result)/len(total)
        pct_per_age.append({'range':str(item[0])+'-'+str(item[1]),
                            'users':len(result),
                            'total':len(total),
                            'pct':100*len(result)/len(total)})

        yesterday_result = Metric.objects.filter(ssn__age__range=(item[0],item[1]),
                                                 date__range=(yesterday_min,yesterday_max)) \
                                         .distinct('ssn__ssn')
        pct_yesterday = 100*len(yesterday_result)/len(total)
        # import pdb;pdb.set_trace()
        pct_change.append({'range':str(item[0])+'-'+str(item[1]),
                           'users_yesterday':len(yesterday_result),
                           'users_today':len(result),
                           'pct_change':pct_today-pct_yesterday,
                           'total':len(total)})
        total_messages = len(Metric.objects.filter(date__range=(today_min,today_max)))
    return {'age_stats_change':pct_change,
            'today_age_stats':pct_per_age,
            'total_messages':total_messages}


def individual_stats(request):
    result = Metric.objects.all().distinct('ssn__ssn')
    total_active = len(result)
    total_people = len(Person.objects.all())

    return render(request,'individual_stats.html',{'total_active':total_active,'total_people':total_people})


def individual_info(request):
    ssn = request.GET.get('ssn')
    if not ssn:
        return JsonResponse({'status':0,'msg':'missing fields'})
    ssn_row = Person.objects.filter(ssn=ssn).first()
    if not ssn_row:
        return JsonResponse({'status':0,'msg':'SSN not found'})
    metrics = Metric.objects.filter(ssn=ssn_row).order_by('-date').values('date','reason','postal_code__postal_code')
    return JsonResponse({'status':1,'data':list(metrics)})
