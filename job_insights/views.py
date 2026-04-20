from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def test_api(request):
    role = request.GET.get('role')
    location = request.GET.get('location')
    if not role:
        return Response({"error": "role is required"}, status=400)
    
    return Response({
        "role": role,
        "location": location
    })