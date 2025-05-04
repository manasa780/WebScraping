from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('scrape/', views.scrape_books, name='scrape_books'),
]
