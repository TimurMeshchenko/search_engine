from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import httpx
from rest_framework.decorators import api_view

class IndexView(APIView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SearchView(APIView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        # Отправлять запрос send_async_request
        # Парсить и через jinja обработать
        return render(request, self.template_name)


@api_view(['POST'])
def get_search_suggestions(request):
    input_value = request.data.get('input_value')
    previous_input_value = request.data.get('previous_input_value')
    url = f'https://yandex.ru/suggest/suggest-ya.cgi?srv=serp_ru_desktop&wiz=TrWth&yu=7762992171731236490&lr=10278&uil=ru&fact=1&v=4&show_experiment=222&show_experiment=224&use_verified=1&safeclick=1&skip_clickdaemon_host=1&rich_nav=1&verified_nav=1&rich_phone=1&use_favicon=1&nav_favicon=1&mt_wizard=1&history=1&nav_text=1&maybe_ads=1&icon=1&hl=1&n=10&portal=1&platform=desktop&mob=0&extend_fw=1&suggest_entity_desktop=1&entity_enrichment=1&entity_max_count=5&svg=1&part={input_value}&pos=0&prev-query={previous_input_value}&hs=0&suggest_reqid=776299217173123649064920435608409'
    method = 'GET'

    return send_async_request(url, method)

def send_async_request(url, method, data=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",        
    }

    if not url:
        return Response({"error": "No URL provided."}, status=400)
    
    try:
        with httpx.Client() as client:
            match method:
                case 'GET':
                    response = client.get(url=url, headers=headers)
                case 'POST':
                    response = client.post(url=url, headers=headers, data=data)
            response.raise_for_status()

        response_data = response.json()

        return Response(response_data)
    except httpx.HTTPStatusError as e:
        return Response({"error": str(e)}, status=e.response.status_code)
    except httpx.RequestError as e:
        return Response({"error": "A network error occurred."}, status=500)
