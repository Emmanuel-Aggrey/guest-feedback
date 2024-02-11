from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from outlets.serializers import CommentSerializer, OutletSerializer
from rest_framework import generics
from outlets.models import Comment, Outlet


class OutletViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
