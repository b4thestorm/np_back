from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from petz.models import Pets, Vaccines
from petz.serializers import MedicalHistorySerializer, PetSerializer, VaccinationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json


class PetsList(APIView):
    def get(self, request, format=None):
        pets = Pets.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, format=None):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PetDetail(APIView):
    def get(self, request, pk, format=None):
        pet = get_object_or_404(Pets, pk=pk)
        serializer = MedicalHistorySerializer(instance=pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        instance = get_object_or_404(Pets, pk=pk)
        serializer = PetSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pet = get_object_or_404(Pets, pk=pk)
        pet.soft_delete()
        return Response(status=status.HTTP_200_OK)
     
    @action(detail=True, methods=['post'])
    def add_vaccine(self, request, pk, format=None):
        pet = get_object_or_404(Pets, pk=pk)
        record = pet.medicalrecord_set.first()
        serializer = VaccinationSerializer(data=request.data)
        if serializer.valid():
            administered = serializer.validated_data.get('administered', None)
            name = serializer.validated_data.get('name', None)
            vaccine = Vaccines(record=record, administered=administered, name=name)
            vaccine.save()
            return Response(status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        

@method_decorator(csrf_exempt, name='dispatch')
class MedicalRecordDetail(APIView):
    def get(self, request, pk):
        try:
            pet = get_object_or_404(Pets, pk=pk)
            serializer = MedicalHistorySerializer(instance=pet)
            return Response(serializer.get_history(pet), status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        pet = Pets.objects.get(id=pk)
        serializer = MedicalHistorySerializer(instance=pet, data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.update(instance=pet, validated_data=json.loads(request.body))
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search(request):
    # take a term or query string of terms and return a queryset built up on that search
    name = request.query_params.get('name', None)
    type = request.query_params.get('type', None)
    results = []
    if name and not type:
        results.append(Pets.objects.filter(name__icontains=name))
    if type and not name:
        results.append(Pets.objects.filter(type=type))
    if name and type:
        results.append(Pets.objects.filter(name__icontains=name).filter(type=type))
    
    serializer = PetSerializer(results.pop(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
