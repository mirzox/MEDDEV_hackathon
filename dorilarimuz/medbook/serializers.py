import os.path

from rest_framework import serializers

from django.conf import settings
from .models import MedBook, Recepts
from app.models import DoctorType
from utils.qr_code import gen_qr_code
from utils.smsservice import Sms
from utils.generatepdf import get_pdf


class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    passport_type = serializers.CharField()
    passport = serializers.CharField()
    full_name = serializers.CharField()
    birth = serializers.IntegerField()


class ReceptPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recepts
        fields = "__all__"


class ReceptGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    m_name = serializers.CharField()
    description = serializers.CharField()
    buyed = serializers.BooleanField()


class MedbookGetserializer(serializers.Serializer):
    id = serializers.IntegerField()
    doctor_id = serializers.CharField(source="doctor_id.full_name")
    doctor_type = serializers.CharField()
    patient_id = PatientSerializer()
    family = serializers.CharField()
    f_name = serializers.CharField()
    diagnoz = serializers.CharField()


class MedbookGetDetailserializer(serializers.Serializer):
    id = serializers.IntegerField()
    doctor_id = DoctorSerializer()
    doctor_type = serializers.CharField()
    patient_id = PatientSerializer()
    family = serializers.CharField()
    f_name = serializers.CharField()
    recept = ReceptGetSerializer(many=True)
    diagnoz = serializers.CharField()
    qr_code = serializers.URLField()
    file = serializers.URLField()


class MedbookPostSerializer(serializers.ModelSerializer):
    recept = ReceptPostSerializer(required=True, many=True)

    class Meta:
        model = MedBook
        fields = ["doctor_id", "patient_id", "family", "diagnoz", "recept"]

    # extra_kwargs = {
    #     "recept": {
    #         "required": True
    #     }
    # }

    def create(self, validated_data):
        recept = validated_data.pop("recept")
        medbook = MedBook.objects.create(**validated_data)
        medbook.doctor_type = DoctorType.objects.get(doctor_id=medbook.doctor_id.id).name.name
        uid = f"{medbook.patient_id.guid}_{medbook.id}"
        qr_url = settings.QR_OUTPUT_PATH.format(f"{uid}.png")
        sms_url = settings.PATIENT_URL.format(uid)
        sms_qr_link = settings.PATIENT_QR_URL.format(f"{uid}.png")
        gen_qr_code(sms_url, qr_url)
        Sms.send_sms(medbook.patient_id.phone_number, f"Ссылка на ваш рецепт: https://api.dorilarim.uz/media/{uid}.pdf\nАдрес ближайшей аптеки: Водород, Чилонзор тумани, Мукимий кучаси.\nТел: 71 273 40 08 ")
        medbook.qr_code = sms_qr_link
        medbook.save()
        t_list = []
        for i in recept:
            temp = Recepts.objects.create(**i)
            medbook.recept.add(temp)
            t_list.append([temp.m_name, temp.description])


        data = {
            "qr_url": qr_url,
            "opath": os.path.join(settings.BASE_DIR, f"media/{uid}.pdf"),
            "p_name": medbook.patient_id.full_name,
            "d_name": medbook.doctor_id.full_name,
            "d_type": medbook.doctor_type,
            "data": t_list
        }
        medbook.file = get_pdf(data)
        medbook.save()
        return medbook


class MedbookReadOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    family = serializers.CharField()
    f_name = serializers.CharField()
    recept = ReceptGetSerializer(many=True)
    diagnoz = serializers.CharField()

    def update(self, instance, validated_data):
        recept_data = validated_data.pop('recept')
        recept = instance.recept

        instance.diagnoz = validated_data.get('diagnoz', instance.diagnoz)
        instance.f_name = validated_data.get('f_name', instance.f_name)

        instance.save()
        for i in recept_data:

            temp = ReceptPostSerializer(Recepts.objects.get(pk=i["id"]), i)
            temp.is_valid(raise_exception=True)
            temp.save()
        return instance
