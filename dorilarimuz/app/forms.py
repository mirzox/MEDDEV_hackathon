from django import forms


class PatientPhoneForm(forms.Form):
    phone = forms.CharField(label='Номер телефона', max_length=13)


class VerifyCode(forms.Form):
    phone = forms.CharField(label='Номер телефона', max_length=13)
    code = forms.CharField(label="Code", max_length=6)


class PatientFieldsForm(forms.Form):
    p_c = (("ID_CARD", "ID CARD"),
           ("BIOMETRIC_PASSPORT", "BIOMETRIC_PASSPORT"),
           ("Водительское", "DRIVER_LICENSE")
           )

    passport_type = forms.ChoiceField(choices=p_c)
    passport = forms.CharField(max_length=20)
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    birth = forms.IntegerField()

