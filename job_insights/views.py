from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os


@api_view(['GET'])
def test_api(request):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    role = request.GET.get("role")

    if not role:
        return Response({"error": "role is required"}, status=400)

    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_APP_KEY"),
        "what": role,
        "results_per_page": 5
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return Response({"error": "Failed to fetch data"}, status=500)
    
    data = response.json()
    
    return Response(data.get("results", []))