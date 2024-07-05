from django.urls import path
from .views import upload_csv, query_data, game_detail

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('query/', query_data, name='query_data'),
    path('game_detail/<int:game_id>/', game_detail, name='game_detail'),
]
