from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView


@api_view()
def hello_world_view(request: Request):
    return Response({"message": "Hello World!"})


class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

