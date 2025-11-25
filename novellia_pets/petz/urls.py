from django.urls import path
from petz import views
from rest_framework.routers import format_suffix_patterns

urlpatterns = [
    path("pets/", views.PetsList.as_view()),
    path("pets/<int:pk>/", views.PetDetail.as_view()),
    path("pets/<int:pk>/medical_records/", views.MedicalRecordDetail.as_view()),
    path("pets/search", views.search),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])