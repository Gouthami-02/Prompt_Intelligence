from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('history/',views.history, name='history'),
    path("delete/<int:id>/", views.delete_prompt, name="delete_prompt"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    
]