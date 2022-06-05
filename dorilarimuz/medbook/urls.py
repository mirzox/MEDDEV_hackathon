from django.urls import path

from .views import MedbookView, MedbookDetailView, PatientMedBookView


urlpatterns = [
    path('', MedbookView.as_view()),
    path('<int:pk>/', MedbookDetailView.as_view()),
    path("<str:guid>/", PatientMedBookView.as_view()),
]
