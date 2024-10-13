from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import json


class IndexView(APIView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SearchView(APIView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        # Отправлять запрос
        # Парсить
        return render(request, self.template_name)