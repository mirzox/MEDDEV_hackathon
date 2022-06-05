from django.db import models

from app.models import User

# Create your models here.


class Recepts(models.Model):
    m_name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    buyed = models. BooleanField(default=False)

    def __str__(self):
        return self.m_name


class MedBook(models.Model):
    family_choices = (
        ("F_M", "Family Member"),
        ("Myself", "myself")
    )

    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="med_doc")
    doctor_type = models.CharField(max_length=256, null=True, blank=True)
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="med_pat")
    family = models.CharField(choices=family_choices, max_length=256, verbose_name="Член Семьи")
    f_name = models.CharField(max_length=256, null=True, blank=True)
    diagnoz = models.CharField(max_length=256)

    recept = models.ManyToManyField(Recepts, verbose_name="Рецепт")
    qr_code = models.URLField(null=True, blank=True)
    file = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_id} {self.patient_id} {self.family}"
