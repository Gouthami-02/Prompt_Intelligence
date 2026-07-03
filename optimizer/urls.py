from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('history/',views.history, name='history'),
    path("delete/<int:id>/", views.delete_prompt, name="delete_prompt"),
]