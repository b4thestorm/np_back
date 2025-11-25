from django.db import models
from django.utils.translation import gettext_lazy as _

class AnimalTypes(models.TextChoices):
    DOG = "DG", "Dog"
    CAT = "CT", "Cat"
    RODENT = "RD", "Rodent"
    RABBIT = "RB", "Rabbits"
    LIZARD = "LZ", "Lizards"
    SNAKE = "SN", "Snakes"
    HORSE = "HR", "Horses"
    TURTLE = "TR", "Turtles"


class VaccineNames(models.TextChoices):
    CANINE_INFLUENZA = "CI", "Canine Influenza"
    LYME_DISEASE = "LD", "Lyme Disease"
    BORDATELLA = "BD", "Bordatella"
    RABIES = "RB", "Rabies"
    PARVOVIRUS = "PV", "Parvovirus"
    PARAINFLUENZA = "PI", "Parainfluenza"
    CANINE_HEPATITIS = "CH", "Canine Hepatitis"
    CANINE_PARAINFLUENZA = "CP", "Canine Parainfluenza"
    DOG_VACCINE = "DV", "Dog Vaccine"
    LEPTOSPIROSIS = "LV", "Leptospirosis Vaccine"
    GIARDIA = "GD", "Giardia"
    KENNEL_COUGH = "KC", "Kennel Cough"

class AllergyName(models.TextChoices):
    POLLEN = "PL", "Pollen"
    DUST_MITES = "DM", "Dust Mites"
    MOLD = "MD", "Mold"
    GRASS = "GR", "Grass"

class ReactionType(models.TextChoices):
    MILD = "MD", "Mild"
    SEVERE = "SV", "Severe"

class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    def soft_deleted(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class Pets(SoftDelete):
    name=models.CharField(max_length=150)
    type=models.CharField(
        max_length=2,
        choices=AnimalTypes.choices,
        default='DG'
    )
    owner=models.CharField(max_length=150)
    dob = models.DateField()

class MedicalRecord(models.Model):
    pet=models.ForeignKey(Pets, on_delete=models.CASCADE)

class Vaccines(models.Model):
    record=models.ForeignKey(MedicalRecord, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(
        max_length=2,
        choices=VaccineNames.choices,
        default='CI'
    )
    administered=models.DateField()

class Allergies(models.Model):
    record=models.ForeignKey(MedicalRecord, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(
        max_length=2,
        choices=AllergyName.choices,
        default='GR'
    )
    reaction=models.CharField(max_length=150)
    severity=models.CharField(
        max_length=2,
        choices=ReactionType.choices,
        default='MD'
    )
     


