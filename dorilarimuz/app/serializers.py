import os
from django.contrib.auth import get_user_model
from django.conf import settings
# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'full_name', 'birth', 'passport_type', "passport", 'new_password']

        extra_kwargs = {
            'password': {
                'write_only': True
             }
        }

    def update(self, instance, validated_data):
        if self.context.get("new_password") is not None:
            instance.set_password(self.context.get("new_password"))
            # instance.save()
        fullname = validated_data.get('full_name', "")
        passport_type = validated_data.get('passport_type', "")
        passport = validated_data.get('passport', "")
        birth = validated_data.get('birth')
        instance.full_name = instance.full_name if fullname == "" else fullname
        instance.passport_type = instance.passport_type if passport_type == "" else passport_type
        instance.passport = instance.passport if passport == "" else passport
        instance.birth = instance.birth if birth == "" else birth
        instance.save()
        return instance


    # def validate_new_password(self, value: str):
    #     length_error = len(value) < 8
    #     digit_error = re.search(r"\d", value) is None
    #     uppercase_error = re.search(r"[A-Z]", value) is None
    #     lowercase_error = re.search(r"[a-z]", value) is None
    #     symbol_error = re.search(r"[!@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', value) is None
    #
    #     if length_error:
    #         raise serializers.ValidationError('password must contain 8 symbols')
    #     elif digit_error:
    #         raise serializers.ValidationError('password must contain digits')
    #     elif lowercase_error:
    #         raise serializers.ValidationError('password must contain at least one lowercase latter')
    #     elif uppercase_error:
    #         raise serializers.ValidationError('password must contain at least one uppercase latter')
    #     elif symbol_error:
    #         raise serializers.ValidationError('password must contain at least one punctuation latter')
    #
    #     return value
class PatientRegisterSerializer(serializers.ModelSerializer):
    passport_choices = (
        ("ID CARD", "ID CARD"),
        ("BIOMETRIC PASSPORT", "BIOMETRIC PASSPORT"),
        ("DRIVER LICENSE", "DRIVER LICENSE")
    )
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    # passport_type = serializers.ChoiceField(choices=passport_choices)
    # passport = serializers.CharField(required=True)
    birth = serializers.IntegerField(required=True)

    class Meta:
        model = get_user_model()
        fields = [
            "phone_number",
            "full_name",
            # 'passport_type',
            # "passport",
            "birth"
        ]

    def validate_phone_number(self, value: str):
        if not value.startswith('998'):
            raise serializers.ValidationError('phone number must start with 998')
        elif len(value) != 12:
            raise serializers.ValidationError('phone must contains 12 digits')
        elif get_user_model().objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('пользователь с таким номером уже существует.')
        return value

    def validator_passport(self, value: str):
        return value.upper()

    def validate_full_name(self, value: str):
        return value.title()

    def validate_birth(self, value: int):
        if len(str(value)) != 4:
            raise serializers.ValidationError("Год рождения должен содержать 4 цифры")
        if value < 1850:
            raise serializers.ValidationError("Не правильный год был введен")
        return value
