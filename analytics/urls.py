from django.urls import path
from .views import upload_csv, query_data

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('query/', query_data, name='query_data'),
]
