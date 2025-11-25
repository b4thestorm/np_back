from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from petz.models import Allergies, Pets, MedicalRecord, Vaccines

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        fields = ['id', 'name', 'type', 'owner', 'dob']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        pet = Pets.objects.create(**validated_data)
        medical_record = MedicalRecord(pet=pet)
        medical_record.save()
        return pet

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = '__all__'

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccines
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)
    vaccinations = VaccinationSerializer(many=True, read_only=True)
    history = serializers.SerializerMethodField()

    class Meta:
        model = Pets
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            medical_record = MedicalRecord.objects.get(pet=instance)
        except ObjectDoesNotExist as e:
            return print(f"{e}")
        
        allergies_data = validated_data.pop('allergies')
        vaccines_data = validated_data.pop('vaccines')

        for allergy in allergies_data:
            a = Allergies(
                record=medical_record,
                name=allergy.get('name'),
                reaction=allergy.get('reaction'),
                severity=allergy.get('severity'),
                )
            a.save()

        for vaccine in vaccines_data:
            v = Vaccines(
                record=medical_record, 
                name=vaccine.get('name'),
                administered=vaccine.get('administered')
            )
            v.save()

        return medical_record
    
    def get_history(self, object):
        record = object.medicalrecord_set.first()
        data = {}
        data['vaccines'] = list(record.vaccines_set.all().values())
        data['allergies'] = list(record.allergies_set.all().values())
        return data
    
    