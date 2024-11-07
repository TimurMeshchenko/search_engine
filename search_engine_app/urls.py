from django.urls import path

from search_engine_app.views import IndexView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
]
