from django.urls import path

from search_engine_app.views import IndexView, SearchView
from .views import get_search_suggestions

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/get_search_suggestions/', get_search_suggestions, name='get_search_suggestions'),
]
