from bs4 import BeautifulSoup
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import httpx
from rest_framework.decorators import api_view
import uuid
import requests
from urllib.parse import urlparse

class IndexView(APIView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SearchView(APIView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        search_request_text = request.GET.get('text', '')
        headers = {
            "Cookie": "_yasc=Dw/vMqjUtGfvC02lZsjEjY7QoIiWHi635gXHmK1P6BjjwfZkfNeFB3L5znH/i4EdzN/aUg==; bh=YMDa0bkGagL6Ow==; i=S1mhN64F4HiWu9HoFz7OpHcib7BZHrj26caVK4EgGs//FDZAzWyPWh4Rscf7GVvA4B/b9Z2V6RC96TrMzqdZhm9M71k=; is_gdpr=0; is_gdpr_b=CI6mChCcngIoAg==; receive-cookie-deprecation=1; spravka=dD0xNjk5OTUzMDc5O2k9MzEuMTQ2LjIwMi4xODg7RD1CMjY1Q0M5ODAzODlDREJFOTJDQzM0QTY4MjdFNUI1RTcyRjIxRURENTVFQzQwNUE0OTc1Qzk3QzMyQTUwMkRGNzRDQTgyODA1NUQ5RDlFNzt1PTE2OTk5NTMwNzk1NDg4MjcyMzY7aD05MGYwOGE3YTkyZjhiYzFkMjc0NWY5OTgzYmEwYWRjOA==; yandexuid=6539346971731489079; yashr=3774455851731489079; ys=wprid.1731489136722416-793728500892691594-balancer-l7leveler-kubr-yp-vla-207-BAL",
            "Postman-Token": str(uuid.uuid4()),
            "User-Agent": "PostmanRuntime/7.42.0",        
        }
        soup = None
        search_results_ul = None

        if not search_request_text:
            return render(request, self.template_name)
    
        while search_request_text:
            try:
                url = f'https://www.yandex.ru/search/?text={search_request_text}'
                search_response = requests.get(url, headers=headers)
                html_content = search_response.text
                
                search_response.raise_for_status()

                soup = BeautifulSoup(html_content, "html.parser")
                search_results_ul = soup.find("ul", id="search-result")

                if not search_results_ul:
                    raise Exception('Captcha')

                break
            except Exception:
                search_request_text = search_request_text[:-1]

        search_results = search_results_ul.find_all("li")
        styles = soup.find_all('style')
        favicon_domain = '//favicon.yandex.net'
        search_items = []
        context = {
            'search_items': search_items
        }

        for search_result in search_results:
            search_result_div = search_result.find('div')
            
            if not search_result_div:
                continue

            search_result_parts = search_result_div.find_all('div', recursive=False)
            search_result_title_index = 0
            search_result_title = None
            
            if not search_result_parts:
                continue

            while not search_result_title and search_result_title_index < len(search_result_parts):
                search_result_title = search_result_parts[search_result_title_index].find('a')
                search_result_title_index += 1

            if not search_result_title:
                continue

            link = search_result_title.get('href')
            search_result_icon = search_result_title.find('div')
            icon_styles = search_result_icon.get('style')
            parsed_link = urlparse(link)
            base_link = f"{parsed_link.scheme}://{parsed_link.netloc}" 

            if icon_styles and 'background-image' not in icon_styles:
                for style in styles:
                    style = style.string
                    if style and base_link in style:
                        icon_link = style.split(favicon_domain)[-1].split(');')[0]
                        icon = f'https://favicon.yandex.net{icon_link}'
                        icon_styles += f';background-image:url("{icon}"'
                        break

            title = search_result_title.find('span').text       
            description = search_result_parts[-1].find('span').text
            search_item = {
                'icon_styles': icon_styles,
                'title': title,
                'link': link[:60],
                'description': description,
            }
            search_items.append(search_item)

        return render(request, self.template_name, context)

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
