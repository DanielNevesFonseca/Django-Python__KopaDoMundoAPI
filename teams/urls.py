from django.urls import path
from .views import TeamView, TeamPerIdView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamPerIdView.as_view())
]
