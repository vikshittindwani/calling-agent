from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/voices/', views.get_voices, name='get_voices'),
    path('api/generate-call/', views.generate_call, name='generate_call'),
    path("media/tts/<str:filename>", views.serve_tts, name="serve_tts"),
]
