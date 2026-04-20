from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
import re


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
    
    total_jobs = len(jobs) if isinstance(jobs, list) else 0

    all_descriptions = []

    for job in jobs:
        desc = job.get("description", "")
        all_descriptions.append(desc.lower())

    skill_keywords = [
        # programming languages
        "python", "java", "c++", "c", "javascript",

        # frameworks / libraries
        "django", "flask", "fastapi", "spring", "react",

        # databases
        "sql", "mysql", "postgresql",

        # tools & platforms
        "docker", "kubernetes", "git", "aws", "azure",

        # data / ai
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"
    ]

    skill_count = {}

    for desc in all_descriptions:
        for skill in skill_keywords:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, desc):
                skill_count[skill] = skill_count.get(skill, 0) + 1

    top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:5]

    all_locations = []

    for job in jobs:
        location = job.get("location", {}).get("display_name", "")
        all_locations.append(location)

    location_count = {}

    for loc in all_locations:
        if loc:
            location_count[loc] = location_count.get(loc, 0) + 1

    top_locations = sorted(location_count.items(), key=lambda x: x[1], reverse=True)[:5]

    average_salary = None

    top_skills_clean = [
        {"skill": skill, "count": count}
        for skill, count in top_skills
    ]

    top_locations_clean = [
        {"location": loc, "count": count}
        for loc, count in top_locations
    ]

    response_data = {
        "summary": {
            "total_jobs": total_jobs
        },
        "insights": {
            "top_skills": top_skills_clean,
            "top_locations": top_locations_clean,
            "average_salary": average_salary
        }
    }
    
    return Response(response_data)