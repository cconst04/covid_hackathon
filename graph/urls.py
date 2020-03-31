from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history', views.history_page, name='history'),
    path('upload', views.upload_file, name='upload'),
    path('today_count_by_region', views.today_count_by_region, name='today_count_by_region'),
    path('get_all_data', views.get_all_data, name='get_all_data'),
    path('load_postal_codes', views.load_postal_codes, name='load_postal_codes'),
    path('load_id_age', views.load_id_age, name='load_id_age'),
    path('per_hour_graph', views.per_hour_graph, name='per_hour_graph'),
]
