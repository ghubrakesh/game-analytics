import io
import ujson
import requests
import numpy as np
import pandas as pd
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import GameData


def upload_csv(request):
    """
    View to handle uploading CSV url to populate GameData model.

    Converts a Google Sheets URL to CSV format and processes the data
    to populate the GameData model.
    It deletes old objects to not cross the limit of free db instance.
    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: Redirects to 'query_data' on successful upload,
                      or error message on failure.
    """

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
                    df = df.replace({np.nan: None})    # Replace all NaN values with None for db compatibility


                    # TODO: HANDLE FOR MULTIPLE USERS: DON'T DELETE THE OLD DATA IF DB LIMIT IS INCREASED.
                    GameData.objects.all().delete()

                    for index, row in df.iterrows():
                        # Format release_date if needed ( Jun 2020 -> Jun 1, 2020)
                        if len(row['Release date']) < 11:
                            row['Release date'] = row['Release date'][:4] + "1, " + row['Release date'][4:]

                        # Create GameData object with parsed data from DataFrame row
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
                    return HttpResponse("No file found at given URL.", status=404)
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")

    return render(request, 'analytics/upload.html')


def query_data(request):
    """
    View to query GameData objects based on user-provided filters.

    Processes POST request parameters to filter GameData objects
    based on various fields like app_id, name, supported age, release date etc.
    Supports multiple filter values for certain fields.

    Args:
        request (HttpRequest): HTTP request object with filter parameters.

    Returns:
        HttpResponse: Rendered 'query.html' template with filtered data.
    """

    data = GameData.objects.all()
    if request.method == 'POST':
        filters = {}
        internal_filter_list = []

        # Process each POST parameter to build filters
        for key, value in request.POST.items():
            if not value or key in ['date_context', 'csrfmiddlewaretoken', 'price_context', 'age_context']:
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
            elif key == 'required_age' and value:
                context = request.POST.get('age_context')
                if context in ['lt', 'gt']:
                    filters[f'required_age__{context}'] = value
                else:
                    filters['required_age'] = value
            elif key in ['supported_languages', 'developers', 'publishers', 'categories', 'tags']:
                # Handle comma-separated values for these fields, make internal django query object and add it to list
                ls = value.split(', ')
                internal_filter = Q()
                for field in ls:
                    internal_filter &= Q(**{f"{key}__icontains": field})
                internal_filter_list.append(internal_filter)
            else:
                if type(value) is str:
                    all_keywords = value.split(',')
                    for kw in all_keywords:
                        filters[f'{key}__icontains'] = value
                else:
                    filters[key] = request.POST[value]

        # Combine internal filters with logical AND, and apply to queryset.
        combined_internal_filter = Q()
        if internal_filter_list:
            for internal_filter in internal_filter_list:
                combined_internal_filter &= internal_filter

        data = GameData.objects.filter(**filters).filter(combined_internal_filter)

    # Return rendered query.html template with data returnd after applying all the filters
    return render(request, 'analytics/query.html', {'data': data})



def game_detail(request, game_id):
    game = get_object_or_404(GameData, pk=game_id)
    return render(request, 'analytics/game_detail.html', {'game': game})
