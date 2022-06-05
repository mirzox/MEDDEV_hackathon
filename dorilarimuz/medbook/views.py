from random import randint, shuffle, choice
import string

from django.http import Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from utils.permitions import HasGroupPermission

from .models import MedBook, Recepts
from . import serializers as srl
from utils.generatepdf import get_pdf

class MedbookView(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'GET': [],
        'POST': []
    }

    def get(self, request):
        # pat_id = request.GET.get('p_id')
        # if pat_id is not None:
        medbook = MedBook.objects.all()
        serializer = srl.MedbookGetserializer(medbook, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(data={"response": "p_id needed"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = srl.MedbookPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedbookDetailView(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'GET': [],
        'POST': []
    }

    def get_data(self, pk: int):
        try:
            return MedBook.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404("Objects doesn't exists")

    def get(self, request, pk: int):
        medbook = self.get_data(pk)
        serializer = srl.MedbookGetDetailserializer(medbook)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int):

        serializer = srl.MedbookReadOnlySerializer(self.get_data(pk), request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data="successfully updated", status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientMedBookView(APIView):

    def get_data(self, p_id, m_id):
        try:
            return MedBook.objects.get(patient_id__guid=p_id, pk=m_id)
        except ObjectDoesNotExist:
            raise Http404("Objects doesn't exists")

    def get(self, request, guid: str):
        print(get_pdf())
        p_id, m_id = guid.split("_")
        medbook = self.get_data(p_id, m_id)
        serializer = srl.MedbookReadOnlySerializer(medbook)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, guid: str):
    #     p_id, m_id = guid.split("_")
    #     serializer = srl.MedbookReadOnlySerializer(self.get_data(p_id, m_id), request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data="successfully updated", status=status.HTTP_200_OK)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)