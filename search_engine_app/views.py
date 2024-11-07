from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import httpx

class IndexView(APIView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SearchView(APIView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        # Отправлять запрос self.send_async_request
        # Парсить и через jinja обработать
        return render(request, self.template_name)


    def send_async_request(self, request):
        url = request.data.get('url')
        method = request.data.get('method')

        if not url:
            return Response({"error": "No URL provided."}, status=400)
        
        try:
            with httpx.Client() as client:
                match method:
                    case 'GET':
                        response = client.get(url)
                    case 'POST':
                        response = client.post(url)
                response.raise_for_status()

            data = response.json()

            return Response(data)
        except httpx.HTTPStatusError as e:
            return Response({"error": str(e)}, status=e.response.status_code)
        except httpx.RequestError as e:
            return Response({"error": "A network error occurred."}, status=500)