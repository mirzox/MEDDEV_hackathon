import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("user_type", User.UserTypeChoices.PATIENT)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", User.UserTypeChoices.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class UserTypeChoices(models.TextChoices):
        ADMIN = _("ADMIN")
        DOCTOR = "DOCTOR"
        PHARMACIST = "PHARMACIST"
        PATIENT = "PATIENT"

    class PassportTypeChoices(models.TextChoices):
        ID_CARD = "ID CARD"
        BIOMETRIC_PASSPORT = "BIOMETRIC PASSPORT"
        DRIVER_LICENSE = "DRIVER LICENSE"

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=12, unique=True)
    user_type = models.CharField(
        choices=UserTypeChoices.choices,
        max_length=15,
    )
    passport_type = models.CharField(
        choices=PassportTypeChoices.choices,
        max_length=20,
        null=True,
        blank=True
    )
    passport = models.CharField(max_length=20, unique=True, verbose_name="Серия и номер пасспорта",
                                null=True, blank=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    birth = models.IntegerField(verbose_name=_("Год рождения"), null=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    # is_verified = models.BooleanField(default=False)
    tg_id = models.IntegerField(null=True, blank=True)
    tg_user = models.CharField(max_length=200, null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.phone_number} {self.id}"


# class Client(models.Model):
#     class PassportTypeChoices(models.TextChoices):
#         ID_CARD = "ID CARD"
#         BIOMETRIC_PASSPORT = "BIOMETRIC PASSPORT"
#         DRIVER_LICENSE = "DRIVER LICENSE"
#
#     guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
#     phone_number = models.CharField(max_length=12, unique=True, verbose_name=_("Номер телефона"))
#     passport_type = models.CharField(
#         choices=PassportTypeChoices.choices,
#         max_length=20
#     )
#     passport = models.CharField(max_length=20, unique=True, verbose_name="Серия и номер пасспорта")
#     firstname = models.CharField(max_length=50, verbose_name=_("first name"))
#     lastname = models.CharField(max_length=50, verbose_name=_("last name"))
#     birth = models.IntegerField(verbose_name=_("Год рождения"))
#     is_verified = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
#
#     class Meta:
#         verbose_name = _("Пациента")
#         verbose_name_plural = _("Пациенты")
#
#     def __str__(self):
#         return f"{self.phone_number}"


class Temp(models.Model):
    phone = models.CharField(max_length=13, unique=True, primary_key=True)
    code = models.CharField(max_length=6)
    attempt = models.IntegerField(default=0)


class DoctorTypeChoices(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name


class DoctorType(models.Model):
    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Врач")
    name = models.ForeignKey(DoctorTypeChoices, on_delete=models.CASCADE, )
    timestamp = models.DateTimeField(auto_now_add=True, auto_created=True)
