# Job Insights API

## Overview
A Django REST API that analyzes job listings based on a given role and returns structured insights such as demand, required skills, and locations.

The system is designed with a layered architecture to minimize redundant external API calls and improve performance using database storage and caching.

## Features

- Query-based API endpoint for job role analysis  
- Integration with external job data source (Adzuna API)  
- Input validation and error handling  
- Data processing to extract:
  - Total number of jobs  
  - Top required skills  
  - Most common job locations  
- Structured JSON response format  
- PostgreSQL database integration for persistent storage  
- Models for storing search queries and processed insights  
- Database-first lookup to reuse previously computed results  
- Redis caching layer for frequently requested queries  
- Cache-first architecture to reduce latency and API usage  
- Multi-layer request handling:
  - Cache → Database → External API  
- Basic logging for cache hits, database hits, and API calls  

## Architecture

```
Request
   ↓
Cache (Redis)
   ↓
Database (PostgreSQL)
   ↓
External API (Adzuna)
```

- Cache is checked first for fastest response  
- If not found, the database is queried  
- If not found in database, data is fetched from external API and processed  
- Results are stored in both database and cache for future requests  


## API Usage

### Endpoint

GET /api/test/?role=<job_role>

### Example

GET /api/test/?role=python

### Sample Response

{
  "summary": {
    "total_jobs": 5
  },
  "insights": {
    "top_skills": [
      {"skill": "python", "count": 3},
      {"skill": "django", "count": 2}
    ],
    "top_locations": [
      {"location": "Bangalore", "count": 2}
    ],
    "average_salary": null
  }
}