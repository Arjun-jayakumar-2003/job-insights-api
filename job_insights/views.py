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
    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return Response({"error": "External API returned an error"}, status=502)
        

        data = response.json()
        if not isinstance(data, dict):
            return Response({"error": "Invalid data format received from API"},status=500)

        jobs = data.get("results", [])

        if not jobs:
            return Response({"message": "No jobs found for the given role"},status=404)
    

        
    except Exception as e:
        return Response({"error": "Failed to fetch job data"},status=500)
    
    return Response(data.get("results", []))