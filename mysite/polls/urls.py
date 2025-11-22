from django.urls import path

from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('poll/<int:poll_id>/', views.poll_details, name='poll_details'),
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),
    path('search/', views.search_polls, name='search_polls'),
    path('poll/<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
    path('create/', views.create_poll, name='create_poll'),
]