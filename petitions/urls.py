from django.urls import path
from . import views

app_name = "petitions"

urlpatterns = [
    path("", views.petition_list_create, name="index"),
    path("<int:pk>/", views.petition_detail, name="detail"),
    path("<int:pk>/vote/", views.petition_vote, name="vote"),
]
