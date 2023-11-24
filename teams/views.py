from django.db import IntegrityError
from django.forms import model_to_dict
from rest_framework.views import (
    APIView, status, Request, Response
)
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from teams.models import Team
from utils import data_processing


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        received_data = request.data

        try:
            data_processing(received_data)
        except NegativeTitlesError:
            return Response({"error": "titles cannot be negative"},
                            status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError:
            return Response({"error": "there was no world cup this year"},
                            status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError:
            return Response({"error": "impossible to have more titles than disputed cups"},
                            status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.create(**received_data)
            return Response(model_to_dict(team), status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "This Fifa code is already registered"},
                            status.HTTP_409_CONFLICT)

    def get(self, request: Request) -> Response:
        all_teams = Team.objects.all()
        converted_all_teams = []
        for team in all_teams:
            dict_team = model_to_dict(team)
            converted_all_teams.append(dict_team)

        return Response(converted_all_teams, status.HTTP_200_OK)


class TeamPerIdView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )
        dict_team = model_to_dict(team)
        return Response(dict_team, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )

        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, team_id: int):
        try:
            team = Team.objects.get(pk=team_id)

        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND
            )

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        return Response(model_to_dict(team), status.HTTP_200_OK)

# return Response({"message": "Delete ok"})
