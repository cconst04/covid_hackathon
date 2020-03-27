from django.http import HttpResponse
from django.shortcuts import render
from os.path import exists,join
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import csv
#templates/examples/dashboard/index.html
def index(request):
    if exists(join(settings.MEDIA_ROOT,settings.CSV_FILENAME)):
        # import pdb;pdb.set_trace()
        # test = pd.read_csv(join(settings.MEDIA_ROOT,settings.CSV_FILENAME))
        with open(join(settings.MEDIA_ROOT,settings.CSV_FILENAME), newline='') as f:
            reader = csv.reader(f,delimiter=',')
            data = list(reader)
        return render(request,'index.html',{'data':data})
    elif request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(settings.CSV_FILENAME, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request,'index.html')
    return render(request,'upload.html')
