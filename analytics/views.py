import ujson
import requests
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import GameData
import io
import numpy as np  # Add this import for handling NaN values

def upload_csv(request):
    if request.method == 'POST':
        url = request.POST.get('csv_url')
        if url:
            try:
                # Convert Google Sheets URL to CSV export URL
                if "docs.google.com/spreadsheets" in url:
                    url = url.replace('/edit?usp=sharing', '/export?format=csv')
                response = requests.get(url)
                if response.status_code == 200:
                    csv_data = response.content.decode('utf-8')
                    df = pd.read_csv(io.StringIO(csv_data))
                    # df = df.where(pd.notna(df), None)
                    df = df.replace({np.nan: None})
                    GameData.objects.all().delete()  # Clear existing data
                    for index, row in df.iterrows():
                        if len(row['Release date']) < 11:
                            row['Release date'] = row['Release date'][:4] + "1, " + row['Release date'][4:]
                        GameData.objects.create(
                            app_id=row['AppID'],
                            name=row['Name'],
                            release_date=datetime.strptime(row['Release date'], '%b %d, %Y'),
                            required_age=row['Required age'],
                            price=row['Price'],
                            dlc_count=row['DLC count'],
                            about_the_game=row['About the game'],
                            supported_languages=row['Supported languages'],
                            windows=row['Windows'],
                            mac=row['Mac'],
                            linux=row['Linux'],
                            positive=row['Positive'],
                            negative=row['Negative'],
                            score_rank=row['Score rank'],
                            developers= ujson.dumps(row['Developers'].split(',')) if row['Developers'] else None,
                            publishers=ujson.dumps(row['Publishers'].split(',')) if row['Publishers'] else None,
                            categories=ujson.dumps(row['Categories'].split(',')) if row['Categories'] else None,
                            genres=ujson.dumps(row['Genres'].split(',')) if row['Genres'] else None,
                            tags=ujson.dumps(row['Tags'].split(',')) if row['Tags'] else None
                        )
                    return redirect('query_data')
                else:
                    return HttpResponse("Failed to download the file. Please check the URL.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")
    return render(request, 'analytics/upload.html')


def query_data(request):
    data = GameData.objects.all()
    if request.method == 'POST':
        filters = {}
        for key, value in request.POST.items():
            if key in ['date_context', 'csrfmiddlewaretoken', 'price_context']:
                continue
            elif key in ['mac', 'windows', 'linux']:
                filters[key] = True
            elif key == 'release_date' and value:
                context = request.POST.get('date_context')
                if context in ['lt', 'gt']:
                    filters[f'release_date__{context}'] = value
                else:
                    filters['release_date'] = value
            elif key == 'price' and value:
                context = request.POST.get('price_context')
                if context in ['lt', 'gt']:
                    filters[f'price__{context}'] = value
                else:
                    filters['price'] = value
            elif key == 'required_age':
                filters[f"{key}__gte"] = value
            elif value:
                if type(value) is str:
                    all_keywords = value.split(',')
                    for kw in all_keywords:
                        filters[f'{key}__icontains'] = value
                else:
                    filters[key] = request.POST[value]
        if filters:
            data = GameData.objects.filter(**filters)
    return render(request, 'analytics/query.html', {'data': data})
