from random import randint, shuffle, choice
import string

from django.http import Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from .models import User, Temp
from . import serializers as srl
from utils.permitions import HasGroupPermission
from utils.smsservice import Sms


class LoginView(ObtainAuthToken):
    # authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # if not request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=user)
        # data = srl.UserSerializer(User.objects.filter(pk=user.pk).prefetch_related('photo'), many=True)
        return Response({
            'token': token.key,
            'phone': user.phone_number
        }, status=status.HTTP_201_CREATED)


class Logout(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({
            'response': 'token successfully deleted'
            }, status=status.HTTP_200_OK
        )


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'GET': [],
        'PUT': []
    }

    def get_data(self, pk):
        try:
            data = User.objects.get(pk=pk)
            # if data.is_superuser:
            #     raise Http404("User not  found!!!")
            return data
        except ObjectDoesNotExist:
            raise Http404("User not  found!!!")

    def get(self, request):
        user = self.get_data(pk=request.user.id)
        # if not request.user.is_staff:
        #     if request.user.id != pk:
        #         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = srl.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_data(pk=request.user.id)
        context = {"new_password": request.data.get("new_password")}
        serializer = srl.UserSerializer(user, data=request.data, partial=True, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendCode(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'POST': []
    }

    def post(self, request):
        phone = request.data.get('phone')
        if phone is None:
            return Response(data={"response": "Номер телефона не передан"}, status=status.HTTP_400_BAD_REQUEST)
        elif len(phone) != 12:
            return Response(data={"response": "Номер должен состять из 12 цифр"}, status=status.HTTP_400_BAD_REQUEST)
        temp, created = Temp.objects.get_or_create(phone=phone)
        if created:
            code = randint(100000, 999999)
            temp.code = str(code)
            temp.save()
            Sms.send_sms(phone=phone, message=f"Ваш код подтверждения: {code}")
        else:
            Sms.send_sms(phone=phone, message=f"Ваш код подтверждения: {temp.code}")
        return Response(data={"response": "СМС успешно отправлен"}, status=status.HTTP_201_CREATED)


class VerifyCode(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'POST': []
    }

    def post(self, request):
        phone = request.data.get('phone')
        temp = Temp.objects.get(phone=phone)
        code = request.data.get('code')

        if temp.code == code:
            temp.delete()
            return Response(data={"response": "Код успешно подтвержден"}, status=status.HTTP_201_CREATED)
        # elif temp.attempt < 5:
        temp.attempt = temp.attempt+1
        temp.save()
        return Response(data={"response": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     temp.delete()
        #     return Response(data={"response": "СМС успешно отправлен"}, status=status.HTTP_400_BAD_REQUEST)


class AddPatient(APIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    authentication_classes = (TokenAuthentication,)

    required_groups = {
        'GET': [],
        'PUT': []
    }
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    def generate_random_password(self):
        length = 13
        shuffle(self.characters)
        password = []
        for i in range(length):
            password.append(choice(self.characters))
        shuffle(password)
        return "".join(password)

    def get(self, request):
        query = request.GET.get('search')
        if query is not None:
            user = User.objects.filter(
                Q(user_type="PATIENT"),
                Q(phone_number__icontains=query) |
                Q(passport__icontains=query.upper()) |
                Q(full_name__icontains=query.title())
            )
            serializer = srl.UserSerializer(user, many=True)
        else:
            user = User.objects.filter(user_type="PATIENT")
            serializer = srl.UserSerializer(user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = srl.PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone_number')
            password = self.generate_random_password()
            User.objects.create_user(password=password, **serializer.validated_data)
            Sms.send_sms(phone=phone, message=f"Ваш пароль:{password} для входа на https://client.dorilarim.uz")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from random import randint
#
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
#
# from .models import Temp, Client
# from .forms import PatientPhoneForm, PatientFieldsForm, VerifyCode
# from utils.smsservice import Sms
#
#
# def get_phone(request):
#     if request.method == "POST":
#         form = PatientPhoneForm(request.POST)
#         if form.is_valid():
#             phone = form.data.get('phone')
#             temp, created = Temp.objects.get_or_create(phone=phone)
#             code = randint(100000, 999999)
#             temp.code = str(code)
#             temp.save()
#             Sms.send_sms(phone=phone[1:], message=f"Ваш код подтверждения: {code}")
#             form = VerifyCode()
#             return render(request, 'verifyphone.html', {'form': form, 'phone': phone})
#     else:
#         form = PatientPhoneForm()
#     return render(request, 'base.html', {'form': form, 'phone': "+998"})
#
#
# # def send_code(request):
# #     # if this is a POST request we need to process the form data
# #     if request.method == 'POST':
# #         # create a form instance and populate it with data from the request:
# #         form = PatientPhoneForm(request.POST)
# #         # check whether it's valid:
# #         if form.is_valid():
# #             phone = form.data.get('phone')
# #             temp, created = Temp.objects.get_or_create(phone=phone)
# #             if created:
# #                 code = randint(100000, 999999)
# #                 temp.code = str(code)
# #                 temp.save()
# #                 Sms.send_sms(phone=phone[1:], message=f"Ваш код подтверждения: {code}")
# #                 form = VerifyCode()
# #                 return render(request, 'verifyphone.html', {'form': form, 'phone': phone})
# #             else:
# #                 code = form.data.get('code')
# #                 if temp.code == code:
# #                     temp.delete()
# #                     form = PatientFieldsForm()
# #                     return render(request, 'index.html', {'form': form, 'phone': phone})
# #                 else:
# #                     pass
# #             form = VerifyCode()
# #
# #             return render(request, 'verifyphone.html', {'form': form, 'phone': phone})
# #     else:
# #         form = PatientPhoneForm()
# #     return render(request, 'base.html', {'form': form, 'phone': "+998"})
#
#
# def verify_phone(request):
#     phone = request.POST.get('phone')
#     if request.method == "POST":
#         form = VerifyCode(request.POST)
#         if form.is_valid():
#             temp = Temp.objects.get(phone=phone)
#             code = form.data.get('code')
#
#             if temp.code == code:
#                 temp.delete()
#                 # form = PatientFieldsForm()
#                 return HttpResponseRedirect(f'/doctor/patient/register/{phone[1:]}/')
#                 # return render(request, 'index.html', {'form': form, 'phone': phone})
#
#         form = VerifyCode()
#         return render(request, 'verifyphone.html', {'form': form, 'phone': phone})
#
#
# def register(request, phone):
#     if request.method == "POST":
#         form = PatientFieldsForm(request.POST)
#         if form.is_valid():
#             Client.objects.create(
#                 phone_number=f"+{phone}",
#                 passport_type=form.data.get("passport_type"),
#                 passport=form.data.get("passport"),
#                 firstname=form.data.get("firstname"),
#                 lastname=form.data.get("lastname"),
#                 birth=form.data.get("birth")
#             )
#             print(form.data)
#             print('post')
#             return render(request, 'index.html', {'form': form, 'phone': f"+{phone}"})
#     print(phone)
#     form = PatientFieldsForm()
#     return render(request, 'index.html', {'form': form, 'phone': f"+{phone}"})



